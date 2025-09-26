#!/usr/bin/env python3
"""Unit tests for Prince George's County boundary polygon utilities.

Converted from pytest style to unittest for consistency with other tests.
"""

import math
import unittest

from check_pg_county import get_pg_county_polygon, is_in_pg


INSIDE_POINTS = [
    (38.9897, -76.9378),  # College Park (UMD)
    (38.9078, -76.8644),  # FedEx Field (Landover)
    (38.7859, -76.7720),  # Upper Marlboro
]

OUTSIDE_POINTS = [
    (38.9847, -77.0947),  # Bethesda (Montgomery County)
    (38.8895, -77.0353),  # National Mall (DC)
    (38.8816, -76.1108),  # Chesapeake Bay east of county
]

INVALID_POINTS = [
    (None, -76.9),
    (38.9, None),
    (float('nan'), -76.9),
    (38.9, float('nan')),
]


class TestPGCountyBoundary(unittest.TestCase):
    """Tests for boundary polygon loading and point-in-polygon logic."""

    @classmethod
    def setUpClass(cls):
        cls.poly = get_pg_county_polygon()

    def test_polygon_loaded(self):
        self.assertIsNotNone(self.poly, "Polygon should load successfully")
        if self.poly is None:  # Defensive guard for static analyzers
            self.fail("County polygon failed to load (None)")
        minx, miny, maxx, maxy = self.poly.bounds
        self.assertGreater(maxx - minx, 0.2, "Polygon bounds width too small; possibly failed load")
        self.assertGreater(maxy - miny, 0.2, "Polygon bounds height too small; possibly failed load")

    def test_inside_points(self):
        for lat, lon in INSIDE_POINTS:
            with self.subTest(point=(lat, lon)):
                self.assertTrue(is_in_pg(lat, lon), f"Expected inside point ({lat},{lon}) to be within PG County")

    def test_outside_points(self):
        for lat, lon in OUTSIDE_POINTS:
            with self.subTest(point=(lat, lon)):
                self.assertFalse(is_in_pg(lat, lon), f"Expected outside point ({lat},{lon}) to be outside PG County")

    def test_invalid_inputs(self):
        for lat, lon in INVALID_POINTS:
            with self.subTest(point=(lat, lon)):
                self.assertFalse(is_in_pg(lat, lon), "Invalid inputs should return False")


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
