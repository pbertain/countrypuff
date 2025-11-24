#!/usr/bin/env python3
"""
Basic usage examples for CountryPuff library.

This script demonstrates how to use CountryPuff to fetch and work with
CIA World Factbook country data.
"""

import sys
import os

# Add the parent directory to the path so we can import countrypuff
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from countrypuff import CountryData, CountryNotFoundError


def main():
    """Demonstrate basic CountryPuff functionality."""
    
    print("🌍 CountryPuff - CIA World Factbook Data Example")
    print("=" * 50)
    
    # Example 1: Get country data by code
    print("\n📍 Example 1: Fetching Nigeria data by country code")
    try:
        nigeria = CountryData.from_code('ni')
        print(f"Country: {nigeria}")
        print(f"Capital: {nigeria.capital}")
        print(f"Population: {nigeria.population}")
        print(f"Area: {nigeria.area_total}")
        print(f"Government Type: {nigeria.government_type}")
    except CountryNotFoundError as e:
        print(f"Error: {e}")
    
    # Example 2: Get country summary
    print("\n📊 Example 2: Country summary")
    try:
        summary = nigeria.summary()
        for key, value in summary.items():
            if value:
                print(f"{key.replace('_', ' ').title()}: {value}")
    except NameError:
        print("Nigeria data not available from previous example")
    
    # Example 3: Access specific sections
    print("\n🏛️ Example 3: Government information")
    try:
        gov_section = nigeria.get_section('Government')
        if gov_section:
            print(f"Independence: {nigeria.independence_date}")
            print(f"Government Type: {nigeria.government_type}")
    except NameError:
        print("Nigeria data not available")
    
    # Example 4: Search within country data
    print("\n🔍 Example 4: Searching for 'oil' in Nigeria data")
    try:
        oil_results = nigeria.search_fields('oil')
        for result in oil_results[:3]:  # Show first 3 results
            path = ' -> '.join(result['path'])
            value = result['value'][:100] + "..." if len(result['value']) > 100 else result['value']
            print(f"Found in {path}: {value}")
    except NameError:
        print("Nigeria data not available")
    
    # Example 5: Try different countries
    print("\n🌎 Example 5: Multiple countries comparison")
    countries_to_try = [
        ('us', 'United States'),
        ('gm', 'Germany'),
        ('ja', 'Japan'),
        ('br', 'Brazil')
    ]
    
    for code, name in countries_to_try:
        try:
            country = CountryData.from_code(code)
            print(f"{name}: Population {country.population}, Capital {country.capital}")
        except CountryNotFoundError:
            print(f"{name}: Data not available")
        except Exception as e:
            print(f"{name}: Error - {e}")
    
    # Example 6: Economic data
    print("\n💰 Example 6: Economic information")
    try:
        print(f"Nigeria GDP per capita: {nigeria.gdp_per_capita}")
        print(f"Nigeria Currency: {nigeria.currency}")
        print(f"Nigeria Exports: {nigeria.exports}")
    except NameError:
        print("Nigeria data not available")
    
    # Example 7: Geographic data
    print("\n🗺️ Example 7: Geographic information")
    try:
        print(f"Location: {nigeria.location}")
        print(f"Climate: {nigeria.climate}")
        print(f"Natural Resources: {nigeria.natural_resources}")
    except NameError:
        print("Nigeria data not available")


def interactive_demo():
    """Interactive demo allowing user to query countries."""
    
    print("\n🎯 Interactive Country Explorer")
    print("Enter country codes (e.g., 'us', 'gm', 'ni') or 'quit' to exit")
    
    while True:
        try:
            user_input = input("\nEnter country code: ").strip().lower()
            
            if user_input in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            
            if not user_input:
                continue
            
            country = CountryData.from_code(user_input)
            
            print(f"\n🏴 {country.name or 'Unknown Country'}")
            print("-" * 30)
            
            summary = country.summary()
            for key, value in summary.items():
                if value:
                    display_key = key.replace('_', ' ').title()
                    print(f"{display_key}: {value}")
            
        except CountryNotFoundError:
            print(f"❌ Country '{user_input}' not found. Try codes like: us, gm, ni, ja, br")
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    # Run basic examples
    main()
    
    # Ask if user wants interactive demo
    try:
        response = input("\nWould you like to try the interactive demo? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            interactive_demo()
    except KeyboardInterrupt:
        print("\nGoodbye! 👋")