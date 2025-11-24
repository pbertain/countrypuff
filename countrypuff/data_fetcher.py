"""
Data fetcher module for retrieving country data from various sources.
"""

import json
import requests
from typing import Dict, List, Optional, Union
from urllib.parse import urljoin
from .country_codes import CountryCodeMapper


class DataFetcher:
    """
    Fetches country data from the factbook.json GitHub repository.
    
    This class provides methods to retrieve country information from the
    comprehensive CIA World Factbook data hosted on GitHub.
    """
    
    BASE_URL = "https://raw.githubusercontent.com/factbook/factbook.json/master/"
    
    # Region mappings
    REGIONS = {
        'africa': 'africa',
        'antarctica': 'antarctica',
        'australia-oceania': 'australia-oceania',
        'central-america-n-caribbean': 'central-america-n-caribbean',
        'central-asia': 'central-asia',
        'east-n-southeast-asia': 'east-n-southeast-asia',
        'europe': 'europe',
        'middle-east': 'middle-east',
        'north-america': 'north-america',
        'south-america': 'south-america',
        'south-asia': 'south-asia',
        'oceans': 'oceans',
        'world': 'world'
    }
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the DataFetcher.
        
        Args:
            timeout: Request timeout in seconds (default: 30)
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CountryPuff/0.1.0 (https://github.com/pbertain/countrypuff)'
        })
        self.code_mapper = CountryCodeMapper()
    
    def get_country_data(self, country_identifier: str, region: Optional[str] = None) -> Dict:
        """
        Fetch country data by country code or name.
        
        Args:
            country_identifier: Country code (e.g., 'us', 'gm') or country name
            region: Optional region to search in (speeds up lookup)
            
        Returns:
            Dictionary containing country data
            
        Raises:
            CountryNotFoundError: If country is not found
            requests.RequestException: If network request fails
        """
        # Convert country name to code if needed
        country_code = self._resolve_country_code(country_identifier.lower())
        
        if region:
            # Try specific region first
            try:
                return self._fetch_from_region(country_code, region)
            except requests.RequestException:
                pass
        
        # Search all regions
        for region_name in self.REGIONS.keys():
            try:
                return self._fetch_from_region(country_code, region_name)
            except requests.RequestException:
                continue
        
        raise CountryNotFoundError(f"Country '{country_identifier}' not found")
    
    def get_countries_by_region(self, region: str) -> List[str]:
        """
        Get list of available countries in a specific region.
        
        Args:
            region: Region name (e.g., 'africa', 'europe')
            
        Returns:
            List of country codes available in the region
            
        Raises:
            ValueError: If region is not valid
        """
        if region not in self.REGIONS:
            raise ValueError(f"Invalid region '{region}'. Valid regions: {list(self.REGIONS.keys())}")
        
        # This would require additional API calls to list directory contents
        # For now, return empty list - could be enhanced later
        return []
    
    def get_all_regions(self) -> List[str]:
        """
        Get list of all available regions.
        
        Returns:
            List of region names
        """
        return list(self.REGIONS.keys())
    
    def _resolve_country_code(self, identifier: str) -> str:
        """
        Resolve country identifier to GEC code using the comprehensive mapping.
        
        Args:
            identifier: Country name, ISO code, or GEC code
            
        Returns:
            GEC code
            
        Raises:
            CountryNotFoundError: If country cannot be resolved
        """
        gec_code = self.code_mapper.resolve_country_code(identifier)
        if gec_code:
            return gec_code
        
        # If no mapping found, raise an error with helpful message
        raise CountryNotFoundError(
            f"Could not resolve '{identifier}' to a valid country code. "
            f"Try using ISO codes (e.g., 'US', 'DE') or full country names (e.g., 'United States', 'Germany')"
        )
    
    def _fetch_from_region(self, country_code: str, region: str) -> Dict:
        """
        Fetch country data from a specific region.
        
        Args:
            country_code: Two-letter country code
            region: Region name
            
        Returns:
            Country data dictionary
            
        Raises:
            requests.RequestException: If request fails
        """
        url = urljoin(self.BASE_URL, f"{region}/{country_code}.json")
        
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        
        return response.json()
    
    def search_countries(self, query: str) -> List[Dict]:
        """
        Search for countries by name.
        
        Args:
            query: Search query
            
        Returns:
            List of matching countries with their information
        """
        results = []
        query_lower = query.lower()
        
        # Search through all country names in the mapping
        for name, iso_code in self.code_mapper.NAME_TO_ISO.items():
            if query_lower in name:
                gec_code = self.code_mapper.iso_to_gec(iso_code)
                if gec_code:
                    try:
                        data = self.get_country_data(gec_code)
                        results.append({
                            'iso_code': iso_code,
                            'gec_code': gec_code,
                            'name': name.title(),
                            'data': data
                        })
                    except:
                        # If we can't fetch data, still include basic info
                        results.append({
                            'iso_code': iso_code,
                            'gec_code': gec_code,
                            'name': name.title(),
                            'data': None
                        })
        
        return results
    
    def list_all_countries(self) -> List[Dict]:
        """
        List all available countries with their codes.
        
        Returns:
            List of dictionaries with country information
        """
        countries = []
        for iso_code, gec_code, name in self.code_mapper.list_all_countries():
            countries.append({
                'iso_code': iso_code,
                'gec_code': gec_code,
                'name': name
            })
        return countries


class CountryNotFoundError(Exception):
    """Raised when a country cannot be found in the data sources."""
    pass