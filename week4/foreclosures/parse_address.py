#!/usr/bin/env python3
"""
Unified address parser - combines the best of both parsing approaches.
This is the definitive address parsing function to use throughout the project.
"""

import re
import csv
import sys

def parse_address(address):
    """
    Parse a street address into components: number, name, unit, kind
    
    Enhanced version that combines robust parsing with clean output for various use cases.
    
    Args:
        address (str): The street address to parse
        
    Returns:
        tuple: (number, name, unit, kind) where:
            - number: House number (e.g., "1600", "123A")
            - name: Street name (e.g., "Pennsylvania", "Main")
            - unit: Unit/apartment info (e.g., "Apt 2B", "#5") or empty string
            - kind: Street type (e.g., "AVE", "ST", "DR") 
        
        Returns (None, None, None, None) if address cannot be parsed.
    """
    if not address:
        return None, None, None, None
    
    # Clean up the address - normalize whitespace
    address = ' '.join(address.split())
    
    # Step 1: Handle comma after number (e.g., "789, Unit 5A Elm Court")
    comma_match = re.match(r'^\s*(\d+(?:[A-Za-z]|[-][A-Za-z])?)\s*,\s*(.+)', address, re.IGNORECASE)
    if comma_match:
        number = comma_match.group(1)
        remainder = comma_match.group(2).strip()
    else:
        # Step 1b: Extract house number normally
        number_match = re.match(r'^\s*(\d+(?:[A-Za-z]|[-][A-Za-z])?)\s+(.+)', address, re.IGNORECASE)
        if not number_match:
            return None, None, None, None
        
        number = number_match.group(1)
        remainder = number_match.group(2).strip()
    
    # Step 2: Look for unit patterns and extract them
    unit = ""
    street_part = remainder
    
    # Unit patterns - more specific ones first
    unit_patterns = [
        (re.compile(r'(.+?)\s+(apt|apartment)\s+([^\s,]+)\s*$', re.IGNORECASE), lambda m: f"{m.group(2)} {m.group(3)}"),
        (re.compile(r'(.+?)\s+(unit)\s+([^\s,]+)\s*$', re.IGNORECASE), lambda m: f"{m.group(2)} {m.group(3)}"),
        (re.compile(r'(.+?)\s+(suite)\s+([^\s,]+)\s*$', re.IGNORECASE), lambda m: f"{m.group(2)} {m.group(3)}"),
        (re.compile(r'(.+?)\s+#([^\s,]+)\s*$', re.IGNORECASE), lambda m: f"#{m.group(2)}"),
        (re.compile(r'(.+?),\s*(.+?)$', re.IGNORECASE), lambda m: m.group(2)),  # Generic comma
    ]
    
    for pattern, extractor in unit_patterns:
        match = pattern.search(remainder)
        if match:
            street_part = match.group(1).strip()
            unit = extractor(match)
            break
    
    # Step 3: Extract street type from the end
    kind = ""
    name = street_part
    
    # Common street types (ordered by length to avoid partial matches)
    street_types = ['STREET', 'AVE', 'AVENUE', 'DRIVE', 'ROAD', 'COURT', 'CIRCLE', 'PLACE', 
                   'LANE', 'BOULEVARD', 'BLVD', 'TERRACE', 'WAY', 'ST', 'DR', 'RD', 'CT', 
                   'CIR', 'PL', 'LN', 'TER']
    
    # Try to find street type at the end
    for street_type in street_types:
        pattern = re.compile(r'^(.+?)\s+' + re.escape(street_type) + r'\s*$', re.IGNORECASE)
        match = pattern.search(street_part)
        if match:
            name = match.group(1).strip().rstrip(',')  # Remove trailing comma
            kind = street_type.upper()
            break
    
    # If no street type found, the whole street_part is the name
    if not kind:
        name = street_part.rstrip(',')  # Remove trailing comma
    
    return number, name, unit, kind


def parse_address_for_geocoding(address):
    """
    Parse address specifically for geocoding APIs.
    
    This is a wrapper around parse_address() that returns a clean format
    suitable for geocoding services (strips unit info that might confuse APIs).
    
    Args:
        address (str): The street address to parse
        
    Returns:
        tuple: (number, name, kind) - simplified for geocoding
    """
    number, name, unit, kind = parse_address(address)
    
    if number is None:
        return None, None, None
    
    # For geocoding, we typically don't want unit information
    # as it can confuse the APIs
    return number, name, kind


def normalize_street_name(street_name, street_type):
    """
    Normalize street names for matching - produces variations for lookup.
    
    Args:
        street_name: The street name (e.g., "Pennsylvania")
        street_type: The street type (e.g., "AVE")
        
    Returns:
        list: List of normalized variations for matching
    """
    if not street_name:
        return []
    
    normalized = street_name.upper().strip()
    variations = [normalized]
    
    # Try with street type appended
    if street_type:
        variations.append(f"{normalized} {street_type.upper()}")
    
    # Try with common abbreviations expanded
    abbreviations = {
        'ST': 'STREET',
        'AVE': 'AVENUE', 
        'DR': 'DRIVE',
        'RD': 'ROAD',
        'CT': 'COURT',
        'CIR': 'CIRCLE',
        'PL': 'PLACE',
        'LN': 'LANE',
        'WAY': 'WAY',
        'BLVD': 'BOULEVARD',
        'TER': 'TERRACE'
    }
    
    if street_type and street_type.upper() in abbreviations:
        expanded = abbreviations[street_type.upper()]
        variations.append(f"{normalized} {expanded}")
    
    return variations


def test_parser():
    """Test the parser with various address formats."""
    test_addresses = [
        "1600 Pennsylvania Ave",
        "123 Main Street",
        "456 Oak Dr Apt 2B",
        "789, Unit 5A Elm Court",
        "321 Pine Lane #12",
        "654 Broadway",  # No street type
        "987A Sunset Blvd",
        "111-B Maple Terrace",
        "222 First St, Suite 100",
        "Invalid Address",
        ""
    ]
    
    print("Testing unified address parser:")
    print("=" * 60)
    
    for addr in test_addresses:
        number, name, unit, kind = parse_address(addr)
        
        print(f"Address: '{addr}'")
        if number is not None:
            print(f"  Number: '{number}', Name: '{name}', Unit: '{unit}', Kind: '{kind}'")
            
            # Test geocoding version
            geo_number, geo_name, geo_kind = parse_address_for_geocoding(addr)
            print(f"  Geocoding: '{geo_number}', '{geo_name}', '{geo_kind}'")
        else:
            print(f"  Could not parse")
        print()


def main():
    """Test with foreclosure data or run tests."""
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_parser()
        return
    
    # Process foreclosure data
    try:
        with open("County_Foreclosures.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            print("number,name,unit,kind")
            
            for row in reader:
                address = row["Street Address"]
                number, name, unit, kind = parse_address(address)
                
                if number is not None:
                    print(f'"{number}","{name}","{unit}","{kind}"')
                else:
                    print(f"Could not parse address: {address}", file=sys.stderr)
                    
    except FileNotFoundError:
        print("County_Foreclosures.csv not found. Run with 'test' argument to see examples.")
        test_parser()


if __name__ == "__main__":
    main()