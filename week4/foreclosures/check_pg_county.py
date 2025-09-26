import json
from shapely.geometry import Point, shape

# Internal cache for the loaded PG County polygon
_PG_POLYGON_CACHE = None

def load_pg_county_polygon(geojson_path: str):
    """
    Loads the Prince George's County boundary from a GeoJSON file.
    
    Args:
        geojson_path: The file path for the GeoJSON boundary file.

    Returns:
        A shapely geometry object representing the county boundary.
    """
    try:
        with open(geojson_path, 'r') as f:
            geojson_data = json.load(f)
        
        # Extract the geometry from the first feature in the FeatureCollection
        if geojson_data['type'] == 'FeatureCollection' and geojson_data['features']:
            geometry = geojson_data['features'][0]['geometry']
            return shape(geometry)
        else:
            raise ValueError("GeoJSON is not a valid FeatureCollection or is empty.")

    except FileNotFoundError:
        print(f"Error: The file '{geojson_path}' was not found.")
        return None
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error reading or parsing GeoJSON file: {e}")
        return None


def is_in_pg_county(latitude: float, longitude: float, county_polygon) -> bool:
    """
    Checks if a latitude/longitude point is inside the Prince George's County polygon.

    Args:
        latitude: The latitude of the point.
        longitude: The longitude of the point.
        county_polygon: The pre-loaded shapely geometry object for the county.

    Returns:
        True if the point is inside the county, False otherwise.
    """
    if county_polygon is None:
        return False
    
    # Check for invalid inputs
    if latitude is None or longitude is None:
        return False
    
    try:
        # Create a shapely Point object. Note the order: (longitude, latitude)
        point = Point(longitude, latitude)
        
        # Use the .contains() method to check for inclusion
        return county_polygon.contains(point)
    except (TypeError, ValueError):
        # Handle any invalid coordinate values (NaN, inf, etc.)
        return False

def get_pg_county_polygon(path: str = 'pg_county_boundary.geojson'):
    """Return cached PG County polygon, loading once if needed."""
    global _PG_POLYGON_CACHE
    if _PG_POLYGON_CACHE is None:
        _PG_POLYGON_CACHE = load_pg_county_polygon(path)
    return _PG_POLYGON_CACHE

def is_in_pg(latitude: float, longitude: float, path: str = 'pg_county_boundary.geojson') -> bool:
    """Convenience wrapper: load (cached) polygon and test point inclusion."""
    polygon = get_pg_county_polygon(path)
    return is_in_pg_county(latitude, longitude, polygon)

# --- Main execution block for demonstration ---
if __name__ == "__main__":
    # Load the county boundary polygon once
    pg_county_shape = load_pg_county_polygon('pg_county_boundary.geojson')

    if pg_county_shape:
        # --- Test Points ---
        
        # 1. College Park, MD (should be True)
        lat_college_park, lon_college_park = 38.9897, -76.9378
        
        # 2. FedEx Field in Landover, MD (should be True)
        lat_fedex, lon_fedex = 38.9077, -76.8645
        
        # 3. Bethesda, MD (should be False)
        lat_bethesda, lon_bethesda = 38.9847, -77.0947

        # --- Perform the checks ---
        is_college_park_in = is_in_pg_county(lat_college_park, lon_college_park, pg_county_shape)
        is_fedex_in = is_in_pg_county(lat_fedex, lon_fedex, pg_county_shape)
        is_bethesda_in = is_in_pg_county(lat_bethesda, lon_bethesda, pg_county_shape)
        
        print(f"Is College Park in PG County? {is_college_park_in}")
        print(f"Is FedEx Field in PG County? {is_fedex_in}")
        print(f"Is Bethesda in PG County? {is_bethesda_in}")
