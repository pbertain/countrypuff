# CountryPuff 🌍

A Python library for accessing comprehensive CIA World Factbook country data. CountryPuff provides easy access to detailed information about countries worldwide, including demographics, geography, economy, government, and more.

## Features

- 🌎 **Comprehensive Data**: Access to 260+ countries and territories
- 📊 **Rich Information**: Demographics, geography, economy, government, military, and more
- 🔍 **Easy Search**: Find countries by name or code
- 🚀 **Simple API**: Intuitive Python interface
- 📈 **Up-to-date**: Data sourced from regularly updated CIA World Factbook
- 🔄 **Multiple Sources**: Supports both factbook.json and CIA API data

## Quick Start

```python
from countrypuff import CountryData

# Get country data by code
nigeria = CountryData.from_code('ni')
print(f"Country: {nigeria.name}")
print(f"Capital: {nigeria.capital}")
print(f"Population: {nigeria.population}")

# Get country summary
summary = nigeria.summary()
for key, value in summary.items():
    if value:
        print(f"{key}: {value}")
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip

### Install from Source

1. Clone the repository:
```bash
git clone https://github.com/pbertain/countrypuff.git
cd countrypuff
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage Examples

### Basic Country Information

```python
from countrypuff import CountryData, CountryNotFoundError

# Fetch country data
try:
    country = CountryData.from_code('us')  # United States
    print(f"Name: {country.name}")
    print(f"Capital: {country.capital}")
    print(f"Population: {country.population}")
    print(f"Area: {country.area_total}")
except CountryNotFoundError:
    print("Country not found")
```

### Economic Data

```python
country = CountryData.from_code('gm')  # Germany
print(f"GDP per capita: {country.gdp_per_capita}")
print(f"Currency: {country.currency}")
print(f"Exports: {country.exports}")
print(f"Imports: {country.imports}")
```

### Geographic Information

```python
country = CountryData.from_code('br')  # Brazil
print(f"Location: {country.location}")
print(f"Climate: {country.climate}")
print(f"Natural Resources: {country.natural_resources}")
print(f"Coordinates: {country.coordinates}")
```

### Government and Demographics

```python
country = CountryData.from_code('ja')  # Japan
print(f"Government Type: {country.government_type}")
print(f"Independence: {country.independence_date}")
print(f"Languages: {country.languages}")
print(f"Religions: {country.religions}")
```

### Advanced Usage

```python
# Get complete sections
geography = country.get_section('Geography')
economy = country.get_section('Economy')

# Search within country data
oil_mentions = country.search_fields('oil')
for result in oil_mentions:
    print(f"Found 'oil' in: {' -> '.join(result['path'])}")

# Access any field using path
population_growth = country.get_field('People and Society', 'Population growth rate', 'text')
```

## Country Codes

CountryPuff uses GEC (formerly FIPS) country codes as used by the CIA World Factbook:

| Country | Code | Country | Code |
|---------|------|---------|------|
| United States | `us` | Germany | `gm` |
| United Kingdom | `uk` | France | `fr` |
| China | `ch` | Japan | `ja` |
| Brazil | `br` | India | `in` |
| Nigeria | `ni` | South Africa | `sf` |

For a complete list, see the [CIA World Factbook Country Codes](https://www.cia.gov/the-world-factbook/references/country-data-codes/).

## Data Sources

CountryPuff fetches data from:

1. **[factbook.json](https://github.com/factbook/factbook.json)** - Primary source with regularly updated JSON data
2. **[CIA World Factbook API](https://github.com/iancoleman/cia_world_factbook_api)** - Alternative source for historical data

## Available Data Categories

- **Introduction**: Background and history
- **Geography**: Location, climate, terrain, natural resources
- **People and Society**: Demographics, languages, religions, education
- **Environment**: Environmental issues, climate data, land use
- **Government**: Political system, leadership, administrative divisions
- **Economy**: GDP, trade, currency, economic indicators
- **Energy**: Electricity, oil, gas, renewable energy
- **Communications**: Internet, telecommunications, media
- **Transportation**: Airports, railways, roads, ports
- **Military and Security**: Armed forces, defense spending
- **Terrorism**: Security threats and terrorist groups
- **Transnational Issues**: Disputes, refugees, trafficking

## Examples

Run the example script to see CountryPuff in action:

```bash
python examples/basic_usage.py
```

This will demonstrate:
- Fetching country data
- Accessing different data categories
- Searching within country information
- Comparing multiple countries

## Development

### Setting up for development

1. Follow the installation steps above
2. Install development dependencies:
```bash
pip install -r requirements-dev.txt  # When available
```

### Running tests

```bash
python -m pytest  # When tests are implemented
```

### Project Structure

```
countrypuff/
├── countrypuff/
│   ├── __init__.py
│   ├── country_data.py      # Main CountryData class
│   └── data_fetcher.py      # Data fetching utilities
├── examples/
│   └── basic_usage.py       # Usage examples
├── requirements.txt
├── README.md
└── LICENSE
```

## Contributing

Contributions are welcome! Here's how you can help:

1. **Report Issues**: Found a bug or have a feature request? Open an issue
2. **Submit Pull Requests**: Fix bugs or add new features
3. **Improve Documentation**: Help make the docs clearer
4. **Add Examples**: Share interesting use cases

### Development Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **CIA World Factbook**: For providing comprehensive country data in the public domain
- **factbook.json project**: For maintaining up-to-date JSON versions of the data
- **CIA World Factbook API**: For historical data access

## Disclaimer

This library provides access to CIA World Factbook data for informational purposes. The data is sourced from public domain materials provided by the Central Intelligence Agency. Users should verify information independently for critical applications.