#!/usr/bin/env python3
"""
Flask web application for CountryPuff - CIA World Factbook data interface.
"""

from flask import Flask, render_template_string, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import json
from typing import Dict, List, Optional

# Import our CountryPuff library
from countrypuff import CountryData, CountryNotFoundError, DataFetcher, CountryCodeMapper

app = Flask(__name__)
CORS(app)  # Enable CORS for API endpoints

# Initialize our data components
data_fetcher = DataFetcher()
code_mapper = CountryCodeMapper()

@app.route('/')
def index():
    """Serve the main HTML page."""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "index.html not found", 404

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files."""
    return send_from_directory('static', filename)

@app.route('/api/countries')
def list_countries():
    """Get list of all available countries."""
    try:
        countries = data_fetcher.list_all_countries()
        return jsonify({
            'success': True,
            'countries': countries
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/countries/search')
def search_countries():
    """Search for countries by name."""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Query parameter "q" is required'
        }), 400
    
    try:
        results = data_fetcher.search_countries(query)
        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/countries/<country_identifier>')
def get_country(country_identifier):
    """Get detailed country data."""
    try:
        # If it's a 2-letter uppercase code, assume it's an ISO code and convert to GEC
        if len(country_identifier) == 2 and country_identifier.isupper():
            gec_code = code_mapper.iso_to_gec(country_identifier)
            if gec_code:
                try:
                    country = CountryData.from_code(gec_code)
                except CountryNotFoundError:
                    # Try as country name
                    country = CountryData.from_name(country_identifier)
            else:
                # Try as country name
                country = CountryData.from_name(country_identifier)
        else:
            # For other formats, try direct lookup first (for GEC codes or names)
            try:
                country = CountryData.from_code(country_identifier)
            except CountryNotFoundError:
                # Try to resolve the country name/code
                resolved_code = code_mapper.resolve_country_code(country_identifier)
                if resolved_code:
                    country = CountryData.from_code(resolved_code)
                else:
                    # Try as country name
                    country = CountryData.from_name(country_identifier)
        
        # Extract comprehensive data
        country_data = {
            # Basic Information
            'name': country.name,
            'official_name': country.official_name,
            'capital': country.capital,
            'population': country.population,
            'area_total': country.area_total,
            'location': country.location,
            'coordinates': country.coordinates,
            'climate': country.climate,
            'natural_resources': country.natural_resources,
            
            # Government
            'government_type': country.government_type,
            'independence_date': country.independence_date,
            
            # Economy
            'currency': country.currency,
            'gdp_per_capita': country.gdp_per_capita,
            'exports': country.exports,
            'imports': country.imports,
            'economic_overview': country.economic_overview,
            'unemployment_rate': country.unemployment_rate,
            
            # Demographics
            'ethnic_groups': country.ethnic_groups,
            'languages': country.languages,
            'religions': country.religions,
            'life_expectancy': country.life_expectancy,
            'age_structure': country.age_structure,
            'birth_rate': country.birth_rate,
            'death_rate': country.death_rate,
            'literacy_rate': country.literacy_rate,
            
            # Communications
            'internet_users': country.internet_users,
            'mobile_phones': country.mobile_phones,
            'broadband_subscriptions': country.broadband_subscriptions,
            
            # Energy
            'electricity_access': country.electricity_access,
            'energy_consumption_per_capita': country.energy_consumption_per_capita,
            'electricity_generation_sources': country.electricity_generation_sources,
            
            # Transportation
            'airports': country.airports,
            'railways': country.railways,
            'ports': country.ports,
            
            # Environment
            'environment_issues': country.environment_issues,
            'air_pollutants': country.air_pollutants,
            
            # Military
            'military_expenditure': country.military_expenditure,
            'military_service_age': country.military_service_age
        }
        
        # Extract the proper ISO code from the CIA Factbook data itself
        internet_country_code = country.get_field('Communications', 'Internet country code', 'text')
        if internet_country_code:
            # Remove the dot from ".cf" to get "cf", then uppercase to get "CF"
            iso_code = internet_country_code.replace('.', '').upper()
            
            # Special mappings for countries where internet code differs from ISO code
            iso_to_flag_mapping = {
                'UK': 'GB',  # United Kingdom uses .uk but flag is GB
                # Add other special cases here if needed
            }
            
            # Use the proper flag code
            flag_code = iso_to_flag_mapping.get(iso_code, iso_code)
            
            country_data['iso_code'] = iso_code
            country_data['flag_url'] = f"https://flagcdn.com/w320/{flag_code.lower()}.png"
        else:
            # Get country code information from mapper as fallback
            country_info = code_mapper.get_country_info(country_identifier)
            if country_info and country_info['iso_code']:
                country_data.update({
                    'iso_code': country_info['iso_code'],
                    'gec_code': country_info['gec_code']
                })
                country_data['flag_url'] = f"https://flagcdn.com/w320/{country_info['iso_code'].lower()}.png"
        
        # Always try to get GEC code for reference
        country_info = code_mapper.get_country_info(country_identifier)
        if country_info:
            country_data['gec_code'] = country_info['gec_code']
        
        return jsonify({
            'success': True,
            'country': country_data,
            'raw_data': country.to_dict()  # Include raw data for debugging
        })
        
    except CountryNotFoundError as e:
        return jsonify({
            'success': False,
            'error': f'Country not found: {str(e)}'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/countries/<country_identifier>/summary')
def get_country_summary(country_identifier):
    """Get country summary data."""
    try:
        country = CountryData.from_code(country_identifier)
        summary = country.summary()
        
        # Add additional info
        country_info = code_mapper.get_country_info(country_identifier)
        if country_info:
            summary.update({
                'iso_code': country_info['iso_code'],
                'gec_code': country_info['gec_code']
            })
            
            if country_info['iso_code']:
                summary['flag_url'] = f"https://flagcdn.com/w320/{country_info['iso_code'].lower()}.png"
        
        return jsonify({
            'success': True,
            'summary': summary
        })
        
    except CountryNotFoundError as e:
        return jsonify({
            'success': False,
            'error': f'Country not found: {str(e)}'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/countries/<country_identifier>/search')
def search_country_fields(country_identifier):
    """Search within a specific country's data."""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Query parameter "q" is required'
        }), 400
    
    try:
        country = CountryData.from_code(country_identifier)
        results = country.search_fields(query)
        
        return jsonify({
            'success': True,
            'country': country.name,
            'query': query,
            'results': results
        })
        
    except CountryNotFoundError as e:
        return jsonify({
            'success': False,
            'error': f'Country not found: {str(e)}'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api')
def api_info():
    """API information and available endpoints."""
    return jsonify({
        'name': 'CountryPuff API',
        'version': '1.0.0',
        'description': 'CIA World Factbook country data API',
        'endpoints': {
            'GET /api/countries': 'List all available countries',
            'GET /api/countries/search?q=<query>': 'Search countries by name',
            'GET /api/countries/<identifier>': 'Get detailed country data',
            'GET /api/countries/<identifier>/summary': 'Get country summary',
            'GET /api/countries/<identifier>/search?q=<query>': 'Search within country data'
        },
        'country_identifiers': 'Use ISO codes (US, DE), GEC codes (us, gm), or country names (United States, Germany)'
    })

@app.route('/curl')
def curl_examples():
    """Plain text cURL examples."""
    base_url = request.url_root.rstrip('/')
    
    examples = f"""CountryPuff API - cURL Examples

# List all countries
curl {base_url}/api/countries

# Search for countries
curl "{base_url}/api/countries/search?q=united"

# Get country data (using ISO code)
curl {base_url}/api/countries/US

# Get country data (using country name)
curl {base_url}/api/countries/Germany

# Get country summary
curl {base_url}/api/countries/NG/summary

# Search within country data
curl "{base_url}/api/countries/BR/search?q=oil"

# API information
curl {base_url}/api
"""
    
    return examples, 200, {'Content-Type': 'text/plain'}

@app.route('/docs')
def docs():
    """API documentation."""
    return jsonify({
        'title': 'CountryPuff API Documentation',
        'description': 'Access comprehensive CIA World Factbook data for countries worldwide',
        'base_url': request.url_root.rstrip('/'),
        'authentication': 'None required',
        'rate_limiting': 'None currently implemented',
        'data_source': 'CIA World Factbook via factbook.json GitHub repository',
        'endpoints': {
            '/api/countries': {
                'method': 'GET',
                'description': 'List all available countries with their codes',
                'response': 'Array of country objects with iso_code, gec_code, and name'
            },
            '/api/countries/search': {
                'method': 'GET',
                'parameters': {'q': 'Search query (required)'},
                'description': 'Search for countries by name',
                'example': '/api/countries/search?q=united'
            },
            '/api/countries/{identifier}': {
                'method': 'GET',
                'description': 'Get comprehensive country data',
                'parameters': {
                    'identifier': 'ISO code (US), GEC code (us), or country name (United States)'
                },
                'response': 'Complete country data including demographics, geography, economy, government'
            },
            '/api/countries/{identifier}/summary': {
                'method': 'GET',
                'description': 'Get key country facts summary',
                'response': 'Condensed country information'
            },
            '/api/countries/{identifier}/search': {
                'method': 'GET',
                'parameters': {'q': 'Search query within country data'},
                'description': 'Search for specific information within a country\'s data'
            }
        }
    })

@app.route('/redoc')
def redoc():
    """ReDoc API documentation interface."""
    # This would typically serve a ReDoc HTML page
    # For now, redirect to the docs endpoint
    return jsonify({
        'message': 'ReDoc interface would be implemented here',
        'alternative': 'Use /docs for API documentation',
        'interactive_testing': 'Use /curl for command-line examples'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'available_endpoints': ['/api', '/docs', '/curl', '/redoc']
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    port = 8000
    print("🌍 Starting CountryPuff Web Server...")
    print(f"📍 Main page: http://localhost:{port}")
    print(f"🔗 API docs: http://localhost:{port}/docs")
    print(f"📋 cURL examples: http://localhost:{port}/curl")
    print(f"🔍 API endpoint: http://localhost:{port}/api")
    
    app.run(debug=True, host='0.0.0.0', port=port)