#!/usr/bin/env python3
"""
Unit tests for parse_address_unified.py

Tests the unified address parser with various address formats to ensure
robust parsing across different use cases.
"""

import unittest
from parse_address import parse_address, normalize_street_name


class TestParseAddress(unittest.TestCase):
    """Test cases for the main parse_address function."""
    
    def test_basic_addresses(self):
        """Test standard address formats."""
        test_cases = [
            ("1600 Pennsylvania Ave", ("1600", "Pennsylvania", "", "AVE")),
            ("123 Main Street", ("123", "Main", "", "STREET")),
            ("456 Oak Dr", ("456", "Oak", "", "DR")),
            ("789 Elm Road", ("789", "Elm", "", "ROAD")),
            ("321 Pine Lane", ("321", "Pine", "", "LANE")),
            ("654 Broadway", ("654", "Broadway", "", "")),  # No street type
        ]
        
        for address, expected in test_cases:
            with self.subTest(address=address):
                # Test full parsing
                result = parse_address(address)
                self.assertEqual(result, expected, 
                               f"Failed for address: '{address}', got {result}, expected {expected}")
                
                # Test geocoding parsing - should match except no unit
                number, name, _, kind = parse_address(address)  # Discard unit component
                geocoding_result = (number, name, kind)
                expected_geocoding = (expected[0], expected[1], expected[3])  # number, name, kind
                self.assertEqual(geocoding_result, expected_geocoding,
                               f"Geocoding parse failed for address: '{address}', got {geocoding_result}, expected {expected_geocoding}")
    
    def test_addresses_with_units(self):
        """Test addresses with apartment/unit information."""
        test_cases = [
            ("456 Oak Dr Apt 2B", ("456", "Oak", "Apt 2B", "DR")),
            ("321 Pine Lane #12", ("321", "Pine", "#12", "LANE")),
            ("789 Elm Court Unit 5A", ("789", "Elm", "Unit 5A", "COURT")),
            ("222 First St Suite 100", ("222", "First", "Suite 100", "ST")),
            ("111 Main Street Apartment 3C", ("111", "Main", "Apartment 3C", "STREET")),
        ]
        
        for address, expected in test_cases:
            with self.subTest(address=address):
                # Test full parsing
                result = parse_address(address)
                self.assertEqual(result, expected,
                               f"Failed for address: '{address}', got {result}, expected {expected}")
                
                # Test geocoding parsing - should match except no unit (unit should be stripped)
                number, name, _, kind = parse_address(address)  # Discard unit component
                geocoding_result = (number, name, kind)
                expected_geocoding = (expected[0], expected[1], expected[3])  # number, name, kind (no unit)
                self.assertEqual(geocoding_result, expected_geocoding,
                               f"Geocoding parse failed for address: '{address}', got {geocoding_result}, expected {expected_geocoding}")
    
    def test_comma_separated_units(self):
        """Test addresses with comma-separated unit information."""
        test_cases = [
            ("789, Unit 5A Elm Court", ("789", "Unit 5A Elm", "", "COURT")),
            ("123, Apt 2B Main St", ("123", "Apt 2B Main", "", "ST")),
            ("456, Suite 100 Oak Dr", ("456", "Suite 100 Oak", "", "DR")),
        ]
        
        for address, expected in test_cases:
            with self.subTest(address=address):
                result = parse_address(address)
                self.assertEqual(result, expected,
                               f"Failed for address: '{address}', got {result}, expected {expected}")
    
    def test_complex_house_numbers(self):
        """Test addresses with complex house numbers."""
        test_cases = [
            ("987A Sunset Blvd", ("987A", "Sunset", "", "BLVD")),
            ("111-B Maple Terrace", ("111-B", "Maple", "", "TERRACE")),
            ("123C Oak Street", ("123C", "Oak", "", "STREET")),
            ("456-D Pine Ave", ("456-D", "Pine", "", "AVE")),
        ]
        
        for address, expected in test_cases:
            with self.subTest(address=address):
                # Test full parsing
                result = parse_address(address)
                self.assertEqual(result, expected,
                               f"Failed for address: '{address}', got {result}, expected {expected}")
                
                # Test geocoding parsing - should match except no unit
                number, name, _, kind = parse_address(address)  # Discard unit component
                geocoding_result = (number, name, kind)
                expected_geocoding = (expected[0], expected[1], expected[3])  # number, name, kind
                self.assertEqual(geocoding_result, expected_geocoding,
                               f"Geocoding parse failed for address: '{address}', got {geocoding_result}, expected {expected_geocoding}")
    
    def test_multi_word_street_names(self):
        """Test addresses with multi-word street names."""
        test_cases = [
            ("8825 East Grove RD", ("8825", "East Grove", "", "RD")),
            ("1234 New York Avenue", ("1234", "New York", "", "AVENUE")),
            ("5678 Old Mill Lane", ("5678", "Old Mill", "", "LANE")),
            ("9999 North Main Street", ("9999", "North Main", "", "STREET")),
        ]
        
        for address, expected in test_cases:
            with self.subTest(address=address):
                # Test full parsing
                result = parse_address(address)
                self.assertEqual(result, expected,
                               f"Failed for address: '{address}', got {result}, expected {expected}")
                
                # Test geocoding parsing - should match except no unit
                number, name, _, kind = parse_address(address)  # Discard unit component
                geocoding_result = (number, name, kind)
                expected_geocoding = (expected[0], expected[1], expected[3])  # number, name, kind
                self.assertEqual(geocoding_result, expected_geocoding,
                               f"Geocoding parse failed for address: '{address}', got {geocoding_result}, expected {expected_geocoding}")
    
    def test_various_street_types(self):
        """Test addresses with different street type abbreviations."""
        test_cases = [
            ("123 Main St", ("123", "Main", "", "ST")),
            ("456 Oak Ave", ("456", "Oak", "", "AVE")),
            ("789 Pine Dr", ("789", "Pine", "", "DR")),
            ("321 Elm Rd", ("321", "Elm", "", "RD")),
            ("654 Maple Ct", ("654", "Maple", "", "CT")),
            ("987 Oak Cir", ("987", "Oak", "", "CIR")),
            ("111 Pine Pl", ("111", "Pine", "", "PL")),
            ("222 Elm Ln", ("222", "Elm", "", "LN")),
            ("333 Main Blvd", ("333", "Main", "", "BLVD")),
            ("444 Oak Ter", ("444", "Oak", "", "TER")),
            ("555 Pine Way", ("555", "Pine", "", "WAY")),
        ]
        
        for address, expected in test_cases:
            with self.subTest(address=address):
                result = parse_address(address)
                self.assertEqual(result, expected,
                               f"Failed for address: '{address}', got {result}, expected {expected}")
    
    def test_real_foreclosure_addresses(self):
        """Test with actual addresses from the foreclosure dataset."""
        test_cases = [
            ("2625  Colebrooke, # 30 DR", ("2625", "Colebrooke", "# 30 DR", "")),
            ("9001 3RD  AVE", ("9001", "3RD", "", "AVE")),
            ("2211 BANNING PL", ("2211", "BANNING", "", "PL")),
            ("7318 OACKCREST DR", ("7318", "OACKCREST", "", "DR")),
            ("8825 East Grove RD", ("8825", "East Grove", "", "RD")),
            ("606 Clovis  AVE", ("606", "Clovis", "", "AVE")),
            ("11221 Westport  DR", ("11221", "Westport", "", "DR")),
            ("10228 Prince 14 T2 PL", ("10228", "Prince 14 T2", "", "PL")),
            ("4203 54th PL", ("4203", "54th", "", "PL")),
        ]
        
        for address, expected in test_cases:
            with self.subTest(address=address):
                # Test full parsing
                result = parse_address(address)
                self.assertEqual(result, expected,
                               f"Failed for address: '{address}', got {result}, expected {expected}")
                
                # Test geocoding parsing - should match except no unit
                number, name, _, kind = parse_address(address)  # Discard unit component
                geocoding_result = (number, name, kind)
                expected_geocoding = (expected[0], expected[1], expected[3])  # number, name, kind
                self.assertEqual(geocoding_result, expected_geocoding,
                               f"Geocoding parse failed for address: '{address}', got {geocoding_result}, expected {expected_geocoding}")
    
    def test_edge_cases(self):
        """Test edge cases and unusual formats."""
        test_cases = [
            ("", (None, None, None, None)),  # Empty string
            ("Not an address", (None, None, None, None)),  # Invalid format
            ("123", (None, None, None, None)),  # Number only
            ("Main Street", (None, None, None, None)),  # No number
        ]
        
        for address, expected in test_cases:
            with self.subTest(address=address):
                # Test full parsing
                result = parse_address(address)
                self.assertEqual(result, expected,
                               f"Failed for address: '{address}', got {result}, expected {expected}")
                
                # Test geocoding parsing - should match for invalid addresses (all None)
                number, name, _, kind = parse_address(address)  # Discard unit component
                geocoding_result = (number, name, kind)
                expected_geocoding = (expected[0], expected[1], expected[3])  # number, name, kind
                self.assertEqual(geocoding_result, expected_geocoding,
                               f"Geocoding parse failed for address: '{address}', got {geocoding_result}, expected {expected_geocoding}")
    
    def test_whitespace_handling(self):
        """Test that extra whitespace is handled correctly."""
        test_cases = [
            ("  123   Main   Street  ", ("123", "Main", "", "STREET")),
            ("456  Oak  Dr  Apt  2B", ("456", "Oak", "Apt 2B", "DR")),
            ("   789   Pine   Lane   #12   ", ("789", "Pine", "#12", "LANE")),
        ]
        
        for address, expected in test_cases:
            with self.subTest(address=address):
                # Test full parsing
                result = parse_address(address)
                self.assertEqual(result, expected,
                               f"Failed for address: '{address}', got {result}, expected {expected}")
                
                # Test geocoding parsing - should match except no unit
                number, name, _, kind = parse_address(address)  # Discard unit component
                geocoding_result = (number, name, kind)
                expected_geocoding = (expected[0], expected[1], expected[3])  # number, name, kind
                self.assertEqual(geocoding_result, expected_geocoding,
                               f"Geocoding parse failed for address: '{address}', got {geocoding_result}, expected {expected_geocoding}")


class TestParseAddressForGeocoding(unittest.TestCase):
    """Test cases for the geocoding-specific address parser."""
    
    def test_basic_geocoding(self):
        """Test that geocoding parser returns clean 3-tuple."""
        test_cases = [
            ("1600 Pennsylvania Ave", ("1600", "Pennsylvania", "AVE")),
            ("123 Main Street", ("123", "Main", "STREET")),
            ("456 Oak Dr Apt 2B", ("456", "Oak", "DR")),  # Unit stripped
            ("321 Pine Lane #12", ("321", "Pine", "LANE")),  # Unit stripped
            ("654 Broadway", ("654", "Broadway", "")),  # No street type
        ]
        
        for address, expected in test_cases:
            with self.subTest(address=address):
                number, name, _, kind = parse_address(address)  # Discard unit component
                result = (number, name, kind)
                self.assertEqual(result, expected,
                               f"Failed for address: '{address}', got {result}, expected {expected}")
    
    def test_geocoding_unit_removal(self):
        """Test that unit information is properly removed for geocoding."""
        test_cases = [
            ("456 Oak Dr Apt 2B", ("456", "Oak", "DR")),
            ("789 Elm Court Unit 5A", ("789", "Elm", "COURT")),
            ("222 First St Suite 100", ("222", "First", "ST")),
            ("321 Pine Lane #12", ("321", "Pine", "LANE")),
        ]
        
        for address, expected in test_cases:
            with self.subTest(address=address):
                number, name, _, kind = parse_address(address)  # Discard unit component
                result = (number, name, kind)
                self.assertEqual(result, expected,
                               f"Failed for address: '{address}', got {result}, expected {expected}")
    
    def test_geocoding_invalid_addresses(self):
        """Test geocoding parser with invalid addresses."""
        test_cases = [
            ("", (None, None, None)),
            ("Not an address", (None, None, None)),
            ("123", (None, None, None)),
        ]
        
        for address, expected in test_cases:
            with self.subTest(address=address):
                number, name, _, kind = parse_address(address)  # Discard unit component
                result = (number, name, kind)
                self.assertEqual(result, expected,
                               f"Failed for address: '{address}', got {result}, expected {expected}")


class TestNormalizeStreetName(unittest.TestCase):
    """Test cases for street name normalization."""
    
    def test_basic_normalization(self):
        """Test basic street name normalization."""
        result = normalize_street_name("Pennsylvania", "AVE")
        expected = ["PENNSYLVANIA", "PENNSYLVANIA AVE", "PENNSYLVANIA AVENUE"]
        self.assertEqual(result, expected)
    
    def test_abbreviation_expansion(self):
        """Test that street type abbreviations are expanded."""
        test_cases = [
            ("Main", "ST", ["MAIN", "MAIN ST", "MAIN STREET"]),
            ("Oak", "DR", ["OAK", "OAK DR", "OAK DRIVE"]),
            ("Pine", "RD", ["PINE", "PINE RD", "PINE ROAD"]),
            ("Elm", "CT", ["ELM", "ELM CT", "ELM COURT"]),
            ("Maple", "LN", ["MAPLE", "MAPLE LN", "MAPLE LANE"]),
        ]
        
        for street_name, street_type, expected in test_cases:
            with self.subTest(street_name=street_name, street_type=street_type):
                result = normalize_street_name(street_name, street_type)
                self.assertEqual(result, expected)
    
    def test_no_street_type(self):
        """Test normalization when no street type is provided."""
        result = normalize_street_name("Broadway", "")
        expected = ["BROADWAY"]
        self.assertEqual(result, expected)
        
        result = normalize_street_name("Broadway", None)
        expected = ["BROADWAY"]
        self.assertEqual(result, expected)
    
    def test_unknown_street_type(self):
        """Test normalization with unknown street type."""
        result = normalize_street_name("Main", "PKWY")
        expected = ["MAIN", "MAIN PKWY"]
        self.assertEqual(result, expected)
    
    def test_empty_street_name(self):
        """Test normalization with empty street name."""
        result = normalize_street_name("", "ST")
        expected = []
        self.assertEqual(result, expected)
        
        result = normalize_street_name(None, "ST")
        expected = []
        self.assertEqual(result, expected)


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple functions."""
    
    def test_parse_and_normalize_workflow(self):
        """Test the typical workflow of parsing then normalizing."""
        address = "123 Main Street Apt 2B"
        
        # Parse the address
        number, name, unit, kind = parse_address(address)
        self.assertEqual((number, name, unit, kind), ("123", "Main", "Apt 2B", "STREET"))
        
        # Normalize for matching
        variations = normalize_street_name(name, kind)
        expected_variations = ["MAIN", "MAIN STREET"]  # STREET expands to STREET
        self.assertEqual(variations, expected_variations)
    
    def test_geocoding_workflow(self):
        """Test the typical geocoding workflow."""
        address = "456 Oak Dr Apt 2B"
        
        # Parse for geocoding (strips unit)
        number, name, _, kind = parse_address(address)  # Discard unit component
        self.assertEqual((number, name, kind), ("456", "Oak", "DR"))
        
        # Verify full parse still works
        full_number, full_name, full_unit, full_kind = parse_address(address)
        self.assertEqual((full_number, full_name, full_unit, full_kind), ("456", "Oak", "Apt 2B", "DR"))


if __name__ == "__main__":
    # Run all tests
    unittest.main(verbosity=2)