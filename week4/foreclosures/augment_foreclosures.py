#!/usr/bin/env python3

import csv
import time
import sys
from parse_address import parse_address
from geocoding_utils import geocode_address_nominatim, is_valid_prince_georges_zip

def augment_foreclosures_csv(input_filename, output_filename):
    """
    Read the foreclosures CSV, geocode missing zip codes, and write augmented version.
    
    Args:
        input_filename: Path to original County_Foreclosures.csv
        output_filename: Path to write augmented CSV
    """
    
    geocoded_count = 0
    skipped_count = 0
    failed_count = 0
    total_processed = 0
    
    print(f"Augmenting {input_filename} -> {output_filename}")
    print("=" * 60)
    
    with open(input_filename, 'r', encoding='utf-8') as infile, \
         open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        
        # Get the fieldnames and ensure we maintain the original structure
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row_num, row in enumerate(reader, start=2):
            total_processed += 1
            
            # Get current zip code
            current_zip = row.get('Zip Code', '').strip()
            street_address = row.get('Street Address', '').strip()
            city = row.get('City', '').strip()
            state = row.get('State', '').strip()
            
            # Check if zip code is missing or invalid (less than 5 digits)
            zip_digits = ''.join(c for c in current_zip if c.isdigit())
            needs_geocoding = len(zip_digits) < 5
            
            if not needs_geocoding:
                # Already has valid zip code, just copy the row
                writer.writerow(row)
                skipped_count += 1
                if total_processed % 1000 == 0:
                    print(f"  Processed {total_processed} rows...")
                continue
            
            # Skip if we don't have enough address info for geocoding
            if not street_address or not city or not state:
                writer.writerow(row)
                failed_count += 1
                continue
            
            print(f"Row {row_num}: Geocoding '{street_address}, {city}, {state}'")
            
            # Parse the street address
            number, name, _, kind = parse_address(street_address)  # Discard unit component
            
            if number is None or name is None:
                print(f"  ✗ Could not parse address")
                writer.writerow(row)  # Write original row
                failed_count += 1
                continue
            
            # Attempt to geocode
            found_zip, confidence = geocode_address_nominatim(number, name, kind, city, state)
            
            # Validate zip code is in Prince George's County
            if found_zip and not is_valid_prince_georges_zip(found_zip):
                print(f"  ⚠ Found zip {found_zip} but it's outside Prince George's County")
                found_zip = None
            
            if found_zip:
                # Update the row with the found zip code
                row['Zip Code'] = found_zip
                print(f"  ✓ Found and updated zip: {found_zip}")
                geocoded_count += 1
            else:
                print(f"  ✗ No valid zip found")
                failed_count += 1
            
            # Write the row (either updated or original)
            writer.writerow(row)
            
            # Progress reporting
            if total_processed % 100 == 0:
                missing_attempted = geocoded_count + failed_count
                print(f"\n--- Progress Update ---")
                print(f"Rows processed: {total_processed:,}")
                print(f"Had zip codes: {skipped_count:,}")
                print(f"Missing zips attempted: {missing_attempted:,}")
                print(f"  ✓ Successfully geocoded: {geocoded_count:,}")
                print(f"  ✗ Failed to geocode: {failed_count:,}")
                if missing_attempted > 0:
                    print(f"  Success rate so far: {geocoded_count/missing_attempted*100:.1f}%")
                print("----------------------\n")
            
            # Be respectful to Nominatim API
            time.sleep(1.0)
    
    # Final summary
    print(f"\n=== AUGMENTATION COMPLETE ===")
    print(f"Total rows processed: {total_processed}")
    print(f"Already had zip codes: {skipped_count}")
    print(f"Successfully geocoded: {geocoded_count}")
    print(f"Failed to geocode: {failed_count}")
    print(f"Output written to: {output_filename}")
    
    if geocoded_count > 0:
        print(f"\nSuccess rate for missing zips: {geocoded_count/(geocoded_count+failed_count)*100:.1f}%")

def count_missing_zips(filename):
    """Count how many rows have missing zip codes."""
    total = 0
    missing = 0
    
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            total += 1
            zip_code = row.get('Zip Code', '').strip()
            zip_digits = ''.join(c for c in zip_code if c.isdigit())
            if len(zip_digits) < 5:
                missing += 1
    
    return total, missing

def main():
    input_file = "County_Foreclosures.csv"
    output_file = "County_Foreclosures_augmented.csv"
    
    # First, count how many need geocoding
    print("Analyzing input file...")
    total_rows, missing_zips = count_missing_zips(input_file)
    
    print("Starting full CSV augmentation with geocoding...")
    print("=" * 60)
    print(f"Total rows in CSV: {total_rows:,}")
    print(f"Rows with missing zip codes: {missing_zips:,}")
    print(f"Percentage missing: {missing_zips/total_rows*100:.1f}%")
    print(f"Estimated time at 1 request/second: {missing_zips/60:.1f} minutes")
    print("=" * 60)
    print("This will take a while due to API rate limiting (1 request per second)")
    print("Press Ctrl+C to stop at any time - partial results will be saved")
    print()
    
    try:
        augment_foreclosures_csv(input_file, output_file)
    except KeyboardInterrupt:
        print(f"\n\nProcess interrupted by user.")
        print(f"Partial results have been saved to {output_file}")
        sys.exit(0)

if __name__ == "__main__":
    main()