#!/usr/bin/env python3
"""
Test script to verify country code mappings are working correctly.
"""

import sys
import os

# Add the parent directory to the path so we can import countrypuff
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from countrypuff import CountryCodeMapper, CountryData, CountryNotFoundError


def test_country_code_mappings():
    """Test the country code mappings mentioned in the user feedback."""
    
    print("🧪 Testing Country Code Mappings")
    print("=" * 40)
    
    # Test cases from user feedback
    test_cases = [
        # (input, expected_gec, expected_name)
        ('KR', 'ks', 'South Korea'),
        ('CF', 'ct', 'Central African Republic'),
        ('ZA', 'sf', 'South Africa'),
        ('ZM', 'za', 'Zambia'),
        ('KI', 'kr', 'Kiribati'),
        ('CG', 'cf', 'Congo'),
        ('US', 'us', 'United States'),
        ('DE', 'gm', 'Germany'),
        ('NG', 'ni', 'Nigeria'),
        ('JP', 'ja', 'Japan'),
    ]
    
    mapper = CountryCodeMapper()
    
    print("\n📋 Testing ISO to GEC mappings:")
    for iso_code, expected_gec, expected_name in test_cases:
        gec_code = mapper.iso_to_gec(iso_code)
        status = "✅" if gec_code == expected_gec else "❌"
        print(f"{status} {iso_code} -> {gec_code} (expected: {expected_gec}) - {expected_name}")
    
    print("\n📋 Testing country name resolution:")
    name_tests = [
        ('South Korea', 'ks'),
        ('Central African Republic', 'ct'),
        ('South Africa', 'sf'),
        ('Zambia', 'za'),
        ('Kiribati', 'kr'),
        ('United States', 'us'),
        ('Germany', 'gm'),
        ('Nigeria', 'ni'),
    ]
    
    for name, expected_gec in name_tests:
        gec_code = mapper.name_to_gec(name)
        status = "✅" if gec_code == expected_gec else "❌"
        print(f"{status} '{name}' -> {gec_code} (expected: {expected_gec})")
    
    print("\n📋 Testing comprehensive resolution:")
    resolution_tests = [
        'KR',  # ISO code
        'ks',  # GEC code
        'South Korea',  # Full name
        'south korea',  # Lowercase name
        'ZA',  # ISO for South Africa
        'sf',  # GEC for South Africa
        'South Africa',  # Name
    ]
    
    for identifier in resolution_tests:
        try:
            gec_code = mapper.resolve_country_code(identifier)
            info = mapper.get_country_info(identifier)
            print(f"✅ '{identifier}' -> {gec_code} ({info['iso_code']}) - {info['name']}")
        except Exception as e:
            print(f"❌ '{identifier}' -> Error: {e}")


def test_data_fetching():
    """Test fetching actual country data with the new mappings."""
    
    print("\n\n🌍 Testing Data Fetching with New Mappings")
    print("=" * 45)
    
    test_countries = [
        ('KR', 'South Korea'),
        ('ZA', 'South Africa'),
        ('ZM', 'Zambia'),
        ('NG', 'Nigeria'),
        ('US', 'United States'),
    ]
    
    for iso_code, name in test_countries:
        try:
            print(f"\n📍 Testing {name} ({iso_code}):")
            
            # Test with ISO code
            country = CountryData.from_code(iso_code)
            print(f"  Name: {country.name}")
            print(f"  Capital: {country.capital}")
            print(f"  Population: {country.population}")
            
            # Test with country name
            country2 = CountryData.from_name(name)
            print(f"  ✅ Both ISO code and name work for {name}")
            
        except CountryNotFoundError as e:
            print(f"  ❌ Error: {e}")
        except Exception as e:
            print(f"  ⚠️  Network/Other Error: {e}")


def test_edge_cases():
    """Test edge cases and error handling."""
    
    print("\n\n🔍 Testing Edge Cases")
    print("=" * 25)
    
    mapper = CountryCodeMapper()
    
    # Test invalid codes
    invalid_tests = ['XX', 'ZZ', 'Invalid Country', '123']
    
    for invalid in invalid_tests:
        result = mapper.resolve_country_code(invalid)
        status = "✅" if result is None else "❌"
        print(f"{status} Invalid '{invalid}' -> {result}")
    
    # Test case sensitivity
    case_tests = [
        ('kr', 'ks'),  # lowercase ISO
        ('KR', 'ks'),  # uppercase ISO
        ('Ks', 'ks'),  # mixed case GEC
        ('south korea', 'ks'),  # lowercase name
        ('SOUTH KOREA', 'ks'),  # uppercase name
    ]
    
    print("\n📋 Testing case sensitivity:")
    for input_code, expected in case_tests:
        result = mapper.resolve_country_code(input_code)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{input_code}' -> {result} (expected: {expected})")


if __name__ == "__main__":
    test_country_code_mappings()
    test_data_fetching()
    test_edge_cases()
    
    print("\n\n🎯 Summary")
    print("=" * 15)
    print("Country code mapping tests completed!")
    print("Check the results above to verify all mappings are working correctly.")