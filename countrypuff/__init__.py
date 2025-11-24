"""
CountryPuff - A Python library for accessing CIA World Factbook country data.

This library provides easy access to comprehensive country information from the
CIA World Factbook, including demographics, geography, economy, government, and more.
"""

from .country_data import CountryData, CountryNotFoundError
from .data_fetcher import DataFetcher
from .country_codes import CountryCodeMapper

__version__ = "0.1.0"
__author__ = "Paul Bertain"
__email__ = "paul+countrypuff@bertain.net"

__all__ = ["CountryData", "CountryNotFoundError", "DataFetcher", "CountryCodeMapper"]