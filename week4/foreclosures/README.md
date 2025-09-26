# Prince George's County Foreclosure Analysis

This project analyzes foreclosure data for Prince George's County, Maryland, providing geocoding, mapping, and visualization tools.

## Python Files

### Main Analysis & Utility Scripts

**Available Python Scripts:**

**`augment_foreclosures.py`**

- **Purpose**: Production tool that creates enhanced dataset with filled zip codes
- **Features**: Uses shared geocoding utilities, batch processing, progress tracking, comprehensive error handling
- **Output**: Geocoded foreclosure dataset (`County_Foreclosures_augmented.csv`)

**`parse_address.py`**

- **Purpose**: Unified address parsing system with comprehensive format support
- **Features**: Handles units/apartments, complex house numbers, multi-word street names, street type normalization
- **Functions**: `parse_address()` for full parsing (returns number, name, unit, kind), `normalize_street_name()` for matching
- **Usage**: Can be run standalone to test parsing or process foreclosure data

**`geocoding_utils.py`**

- **Purpose**: Shared geocoding utility functions
- **Functions**: `geocode_address_nominatim()` (Nominatim API geocoding), `is_valid_prince_georges_zip()` (zip code validation)
- **Usage**: Imported by geocoding scripts to provide consistent geocoding logic

**`test_parse_address.py`**

- **Purpose**: Comprehensive unit tests for the address parser
- **Coverage**: Basic addresses, units, edge cases, real foreclosure data, geocoding workflows
- **Usage**: Run with `python test_parse_address.py`

**`check_geocoding_missing_zips.py`**

- **Purpose**: Analysis tool for testing geocoding success rates on foreclosure records missing zip codes (read-only)
- **Features**: Uses shared geocoding utilities, handles rate limiting, unified address parsing, validates zip codes are in Prince George's County
- **Output**: Creates analysis CSV with geocoding results, does not modify original data

### Prince George's County Boundary Checking

**`check_pg_county.py`**

- **Purpose**: Tests if coordinates are within Prince George's County boundaries
- **Features**: Loads county boundary from GeoJSON, performs point-in-polygon tests
- **Functions**: `is_in_pg()` for coordinate validation, `load_pg_county_polygon()` for boundary loading
- **Usage**: Used by other scripts to validate geographic locations

**`test_pg_boundary.py`**

- **Purpose**: Unit tests for Prince George's County boundary checking
- **Coverage**: Tests known inside/outside points and invalid input handling
- **Usage**: Run with `python test_pg_boundary.py`

## Key Datasets

**`County_Foreclosures.csv`** - Main foreclosure dataset  
**`ACSDP5Y2020.DP04-Data.csv`** - 2020 DP04 ACS housing data 
**`Prince_Georges_County_Maintained_Roads_-7480761036642557875.geojson`** - Official county road data  
**`pg_county_boundary.geojson`** - Prince George's County boundary for geographic validation

## Usage Examples

```bash
# Run address parser unit tests
uv run python test_parse_address.py

# Run boundary checking unit tests  
uv run python test_pg_boundary.py

# Test geocoding on missing zip codes (creates analysis CSV)
uv run python test_geocoding_missing_zips.py

# Augment foreclosure data with geocoded zip codes
uv run python augment_foreclosures.py

# Test address parsing
uv run python -c "from parse_address import parse_address; print(parse_address('123 Main St Apt 2B'))"

# Test boundary checking
uv run python -c "from check_pg_county import is_in_pg; print(is_in_pg(38.9897, -76.9378))"  # College Park (should be True)
```

## Architecture

The system provides:

1. **Address parsing**: Robust parsing of street addresses with unit support
2. **Geocoding utilities**: Nominatim API integration with rate limiting and validation
3. **Geographic validation**: Prince George's County boundary checking using authoritative polygon data
4. **Data augmentation**: Tools to fill missing zip codes in foreclosure datasets

## Dependencies

The project uses the following Python libraries:

- **`requests`** - HTTP client for geocoding API calls (Nominatim)
- **`shapely`** - Geometric operations for boundary checking (point-in-polygon tests)

Install dependencies with:

```bash
uv sync
```

## Main Python Methods Overview

### Address Parsing and Geocoding

- `parse_address.py`
  - `parse_address()`: Parses street addresses into components (number, name, unit, kind)
  - `normalize_street_name()`: Creates variations for address matching
  - `test_parser()`: Quick test for address parsing logic

- `geocoding_utils.py`
  - `geocode_address_nominatim()`: Geocodes addresses using OpenStreetMap Nominatim API
  - `is_valid_prince_georges_zip()`: Validates if zip code is in Prince George's County

### Data Augmentation

- `augment_foreclosures.py`
  - `augment_foreclosures_csv()`: Fills missing zip codes in foreclosure data using geocoding
  - `count_missing_zips()`: Analyzes how many records need geocoding

### Testing and Analysis

- `check_geocoding_missing_zips.py`
  - `find_missing_zip_codes()`: Tests geocoding success rates on missing zip codes
  - `print_summary()`: Summarizes geocoding results

### Geographic Boundary Validation

- `check_pg_county.py`
  - `load_pg_county_polygon()`: Loads county boundary from GeoJSON
  - `is_in_pg_county()`: Tests if coordinates are within Prince George's County
  - `get_pg_county_polygon()`: Cached polygon loading

### Unit Tests

- `test_parse_address.py`: Comprehensive address parsing tests
- `test_pg_boundary.py`: Geographic boundary validation tests

For more details, see the docstrings in each file or the function definitions themselves.
