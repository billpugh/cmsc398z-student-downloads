#!/usr/bin/env python3

import csv
import time
import sys
from parse_address import parse_address
from geocoding_utils import geocode_address_nominatim, is_valid_prince_georges_zip


def find_missing_zip_codes(filename, max_attempts=100):
    """
    Find foreclosure entries with missing zip codes and attempt to geocode them.
    
    This is an analysis tool that creates a CSV with geocoding results but doesn't
    modify the original data.
    
    Args:
        filename: Path to the foreclosure CSV file
        max_attempts: Maximum number of geocoding attempts for testing
        
    Returns:
        List of dictionaries with geocoding results
    """
    results = []
    attempts = 0
    
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, start=2):
            # Stop if we've reached our max attempts
            if attempts >= max_attempts:
                print(f"Reached maximum attempts ({max_attempts}). Stopping.")
                break
                
            # Check if zip code is missing or invalid
            zip_code = row.get('Zip Code', '').strip()
            street_address = row.get('Street Address', '').strip()
            city = row.get('City', '').strip()
            state = row.get('State', '').strip()
            
            # Skip if we have a valid zip code (5 digits)
            zip_digits = ''.join(c for c in zip_code if c.isdigit())
            if len(zip_digits) >= 5:
                continue
                
            # Skip if we don't have enough address info
            if not street_address or not city or not state:
                print(f"Row {row_num}: Insufficient address data - {street_address}, {city}, {state}")
                continue
            
            print(f"Row {row_num}: Missing zip for '{street_address}, {city}, {state}'")
            
            # Parse the street address
            number, name, unit, kind = parse_address(street_address)
            # For geocoding, we only use number, name, kind (discard unit)
            
            if number is None or name is None:
                print(f"Row {row_num}: Could not parse address '{street_address}'")
                continue
            
            print(f"  Parsed: {number} {name} {kind}")
            
            # Use Nominatim geocoding from shared utilities
            print(f"trying Nominatim...")
            found_zip, confidence = geocode_address_nominatim(number, name, kind, city, state)
            api_used = "Nominatim"
            
            # Validate zip code if found
            is_valid_pg_zip = False
            if found_zip:
                is_valid_pg_zip = is_valid_prince_georges_zip(found_zip)
            
            # Add a longer delay for Nominatim to be respectful
            time.sleep(1.0)
            
            attempts += 1
            
            result = {
                'row_number': row_num,
                'original_address': street_address,
                'city': city,
                'state': state,
                'parsed_number': number,
                'parsed_name': name,
                'parsed_kind': kind,
                'found_zip': found_zip,
                'confidence': confidence,
                'api_used': api_used,
                'original_zip': zip_code,
                'is_valid_pg_zip': is_valid_pg_zip
            }
            
            results.append(result)
            
            if found_zip:
                validity_note = " (✓ Valid PG zip)" if is_valid_pg_zip else " (⚠ Not a PG zip)"
                print(f"  ✓ Found zip: {found_zip} (confidence: {confidence}){validity_note}")
            else:
                print(f"  ✗ No zip found")
    
    return results


def print_summary(results):
    """Print a summary of geocoding results."""
    total = len(results)
    found = sum(1 for r in results if r['found_zip'])
    not_found = total - found
    valid_pg = sum(1 for r in results if r['found_zip'] and r['is_valid_pg_zip'])
    
    print(f"\n=== GEOCODING SUMMARY ===")
    print(f"Total addresses processed: {total}")
    print(f"Zip codes found: {found} ({found/total*100:.1f}%)")
    print(f"Valid Prince George's County zips: {valid_pg} ({valid_pg/total*100:.1f}%)")
    print(f"Zip codes not found: {not_found} ({not_found/total*100:.1f}%)")
    
    if found > 0:
        print(f"\n=== SUCCESSFUL MATCHES ===")
        for result in results:
            if result['found_zip']:
                validity_note = " (✓ Valid PG)" if result['is_valid_pg_zip'] else " (⚠ Not PG)"
                print(f"Row {result['row_number']}: {result['original_address']}, {result['city']}, {result['state']} → {result['found_zip']}{validity_note}")
    
    if not_found > 0:
        print(f"\n=== FAILED MATCHES ===")
        for result in results:
            if not result['found_zip']:
                print(f"Row {result['row_number']}: {result['original_address']}, {result['city']}, {result['state']}")


def save_results_to_csv(results, output_filename="geocoding_results.csv"):
    """Save geocoding results to a CSV file."""
    if not results:
        print("No results to save.")
        return
    
    with open(output_filename, 'w', newline='', encoding='utf-8') as file:
        fieldnames = [
            'row_number', 'original_address', 'city', 'state',
            'parsed_number', 'parsed_name', 'parsed_kind',
            'found_zip', 'confidence', 'api_used', 'original_zip', 'is_valid_pg_zip'
        ]
        
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Results saved to {output_filename}")


def main():
    filename = "County_Foreclosures.csv"
    
    print("Starting geocoding analysis of missing zip codes...")
    print("Using OpenStreetMap Nominatim API via shared geocoding utilities")
    print("=" * 60)
    
    # Run analysis with validation for Prince George's County zip codes
    results = find_missing_zip_codes(filename, max_attempts=50)
    
    # Print summary
    print_summary(results)
    
    # Save results to CSV
    save_results_to_csv(results)


if __name__ == "__main__":
    main()