#!/usr/bin/env python3

import requests
import sys


def geocode_address_nominatim(street_number, street_name, street_type, city, state):
    """
    Geocode using OpenStreetMap Nominatim API.
    
    Args:
        street_number: House number
        street_name: Street name
        street_type: Street type (St, Ave, etc.) - can be None
        city: City name
        state: State name
        
    Returns:
        tuple: (zip_code, confidence_score) or (None, None) if not found
    """
    # Construct the full address
    if street_type:
        full_address = f"{street_number} {street_name} {street_type}, {city}, {state}, USA"
    else:
        full_address = f"{street_number} {street_name}, {city}, {state}, USA"
    
    # Nominatim API endpoint
    base_url = "https://nominatim.openstreetmap.org/search"
    
    # Parameters for the API call
    params = {
        'q': full_address,
        'format': 'json',
        'addressdetails': 1,
        'limit': 1
    }
    
    # Add a User-Agent header (required by Nominatim)
    headers = {
        'User-Agent': 'ForeclosureAnalysis/1.0 (educational use)'
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        if data and len(data) > 0:
            result = data[0]
            address_details = result.get('address', {})
            
            # Try different fields where zip code might be stored
            zip_code = (address_details.get('postcode') or 
                       address_details.get('postal_code'))
            
            if zip_code:
                # Use importance as confidence score (0-1)
                importance = float(result.get('importance', 0))
                return zip_code, importance
        
        return None, None
        
    except requests.RequestException as e:
        print(f"Nominatim API request failed: {e}", file=sys.stderr)
        return None, None
    except Exception as e:
        print(f"Error processing Nominatim response: {e}", file=sys.stderr)
        return None, None


def is_valid_prince_georges_zip(zip_code):
    """Check if zip code is in Prince George's County."""
    # Known Prince George's County zip codes
    valid_zip_codes = {
        '20601', '20607', '20608', '20613', '20623', '20705', '20706', '20707', 
        '20708', '20710', '20712', '20715', '20716', '20720', '20721', '20722', 
        '20735', '20737', '20740', '20742', '20743', '20744', '20745', '20746', 
        '20747', '20748', '20762', '20769', '20770', '20772', '20774', '20781', 
        '20782', '20783', '20784', '20785', '20903', '20904', '20912'
    }
    return zip_code in valid_zip_codes