"""
Country data model and utilities for working with CIA World Factbook data.
"""

from typing import Dict, List, Optional, Any, Union
from .data_fetcher import DataFetcher, CountryNotFoundError


class CountryData:
    """
    Represents country data from the CIA World Factbook.
    
    This class provides a convenient interface for accessing and working with
    country information including demographics, geography, economy, government, etc.
    """
    
    def __init__(self, data: Optional[Dict] = None, country_code: Optional[str] = None):
        """
        Initialize CountryData.
        
        Args:
            data: Raw country data dictionary
            country_code: Country code to fetch data for (if data not provided)
        """
        self._data = data or {}
        self._fetcher = DataFetcher()
        
        if not data and country_code:
            self._data = self._fetcher.get_country_data(country_code)
    
    @classmethod
    def from_code(cls, country_code: str) -> 'CountryData':
        """
        Create CountryData instance from country code.
        
        Args:
            country_code: Two-letter country code (e.g., 'us', 'gm')
            
        Returns:
            CountryData instance
        """
        return cls(country_code=country_code)
    
    @classmethod
    def from_name(cls, country_name: str) -> 'CountryData':
        """
        Create CountryData instance from country name.
        
        Args:
            country_name: Country name (e.g., 'United States', 'Germany')
            
        Returns:
            CountryData instance
        """
        fetcher = DataFetcher()
        data = fetcher.get_country_data(country_name)
        return cls(data=data)
    
    # Basic Information Properties
    @property
    def name(self) -> Optional[str]:
        """Get the country's conventional short form name."""
        short_name = self._get_nested_value(['Government', 'Country name', 'conventional short form', 'text'])
        # If short form is "none" or empty, fall back to long form
        if not short_name or short_name.lower() == 'none':
            return self._get_nested_value(['Government', 'Country name', 'conventional long form', 'text'])
        return short_name
    
    @property
    def official_name(self) -> Optional[str]:
        """Get the country's conventional long form name."""
        return self._get_nested_value(['Government', 'Country name', 'conventional long form', 'text'])
    
    @property
    def capital(self) -> Optional[str]:
        """Get the country's capital city."""
        return self._get_nested_value(['Government', 'Capital', 'name', 'text'])
    
    @property
    def population(self) -> Optional[str]:
        """Get the country's total population."""
        return self._get_nested_value(['People and Society', 'Population', 'total', 'text'])
    
    @property
    def area_total(self) -> Optional[str]:
        """Get the country's total area."""
        return self._get_nested_value(['Geography', 'Area', 'total ', 'text']) or \
               self._get_nested_value(['Geography', 'Area', 'total', 'text'])
    
    @property
    def gdp_per_capita(self) -> Optional[str]:
        """Get the country's GDP per capita."""
        return self._get_nested_value(['Economy', 'Real GDP per capita', 'Real GDP per capita 2024', 'text']) or \
               self._get_nested_value(['Economy', 'Real GDP per capita', 'Real GDP per capita 2023', 'text'])
    
    # Geography Properties
    @property
    def location(self) -> Optional[str]:
        """Get the country's geographic location description."""
        return self._get_nested_value(['Geography', 'Location', 'text'])
    
    @property
    def coordinates(self) -> Optional[str]:
        """Get the country's geographic coordinates."""
        return self._get_nested_value(['Geography', 'Geographic coordinates', 'text'])
    
    @property
    def climate(self) -> Optional[str]:
        """Get the country's climate description."""
        return self._get_nested_value(['Geography', 'Climate', 'text'])
    
    @property
    def natural_resources(self) -> Optional[str]:
        """Get the country's natural resources."""
        return self._get_nested_value(['Geography', 'Natural resources', 'text'])
    
    # Demographics Properties
    @property
    def ethnic_groups(self) -> Optional[str]:
        """Get the country's ethnic groups breakdown."""
        return self._get_nested_value(['People and Society', 'Ethnic groups', 'text'])
    
    @property
    def languages(self) -> Optional[str]:
        """Get the country's languages."""
        return self._get_nested_value(['People and Society', 'Languages', 'text'])
    
    @property
    def religions(self) -> Optional[str]:
        """Get the country's religions breakdown."""
        return self._get_nested_value(['People and Society', 'Religions', 'text'])
    
    @property
    def life_expectancy(self) -> Optional[str]:
        """Get the country's life expectancy."""
        return self._get_nested_value(['People and Society', 'Life expectancy at birth', 'total population', 'text'])
    
    # Government Properties
    @property
    def government_type(self) -> Optional[str]:
        """Get the country's government type."""
        return self._get_nested_value(['Government', 'Government type', 'text'])
    
    @property
    def independence_date(self) -> Optional[str]:
        """Get the country's independence date."""
        return self._get_nested_value(['Government', 'Independence', 'text'])
    
    # Economy Properties
    @property
    def economic_overview(self) -> Optional[str]:
        """Get the country's economic overview."""
        return self._get_nested_value(['Economy', 'Economic overview', 'text'])
    
    @property
    def currency(self) -> Optional[str]:
        """Get the country's currency."""
        return self._get_nested_value(['Economy', 'Exchange rates', 'Currency', 'text'])
    
    @property
    def exports(self) -> Optional[str]:
        """Get the country's export value."""
        return self._get_nested_value(['Economy', 'Exports', 'Exports 2024', 'text']) or \
               self._get_nested_value(['Economy', 'Exports', 'Exports 2023', 'text'])
    
    @property
    def imports(self) -> Optional[str]:
        """Get the country's import value."""
        return self._get_nested_value(['Economy', 'Imports', 'Imports 2024', 'text']) or \
               self._get_nested_value(['Economy', 'Imports', 'Imports 2023', 'text'])
    
    # Utility Methods
    def get_section(self, section_name: str) -> Optional[Dict]:
        """
        Get a complete section of country data.
        
        Args:
            section_name: Name of the section (e.g., 'Geography', 'Economy')
            
        Returns:
            Dictionary containing the section data
        """
        return self._data.get(section_name)
    
    def get_field(self, *path: str) -> Optional[Any]:
        """
        Get a specific field using a path.
        
        Args:
            *path: Path to the field (e.g., 'Geography', 'Area', 'total', 'text')
            
        Returns:
            Field value or None if not found
        """
        return self._get_nested_value(list(path))
    
    def search_fields(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for fields containing a specific query.
        
        Args:
            query: Search query
            
        Returns:
            List of matching fields with their paths and values
        """
        results = []
        query_lower = query.lower()
        
        def search_recursive(data: Any, path: List[str] = None) -> None:
            if path is None:
                path = []
            
            if isinstance(data, dict):
                for key, value in data.items():
                    current_path = path + [key]
                    if isinstance(value, str) and query_lower in value.lower():
                        results.append({
                            'path': current_path,
                            'value': value
                        })
                    elif isinstance(value, (dict, list)):
                        search_recursive(value, current_path)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    search_recursive(item, path + [str(i)])
        
        search_recursive(self._data)
        return results
    
    def to_dict(self) -> Dict:
        """
        Get the raw country data as a dictionary.
        
        Returns:
            Raw country data dictionary
        """
        return self._data.copy()
    
    def summary(self) -> Dict[str, Optional[str]]:
        """
        Get a summary of key country information.
        
        Returns:
            Dictionary with key country facts
        """
        return {
            'name': self.name,
            'official_name': self.official_name,
            'capital': self.capital,
            'population': self.population,
            'area': self.area_total,
            'location': self.location,
            'government_type': self.government_type,
            'currency': self.currency,
            'gdp_per_capita': self.gdp_per_capita
        }
    
    def _get_nested_value(self, path: List[str]) -> Optional[Any]:
        """
        Get a nested value from the data using a path.
        
        Args:
            path: List of keys representing the path to the value
            
        Returns:
            The value at the path or None if not found
        """
        current = self._data
        
        for key in path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        
        return current
    
    def __str__(self) -> str:
        """String representation of the country."""
        name = self.name or "Unknown Country"
        capital = self.capital
        population = self.population
        
        result = f"{name}"
        if capital:
            result += f" (Capital: {capital})"
        if population:
            result += f" - Population: {population}"
        
        return result
    
    def __repr__(self) -> str:
        """Developer representation of the country."""
        name = self.name or "Unknown"
        return f"CountryData(name='{name}')"