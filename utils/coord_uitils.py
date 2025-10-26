import re
from typing import Tuple, Optional
from geopy.geocoders import Nominatim
from geopy.point import Point
import os
import time

geolocator = Nominatim(user_agent="claims_verifier_app")

def parse_latlon(text: str) -> Optional[Tuple[float, float]]:
    """
    Accepts formats:
      1."lat, lon"
      2."lat lon"
      3."POINT(lat lon)"
      4.decimal degrees with +/- signs
    Returns Option<(float,float), None>.
    """
    text = text.strip()
    m = re.search(r'(-?\d+\.\d+)\s*[,\s]\s*(-?\d+\.\d+)', text)
    if m: return float(m.group(1)), float(m.group(2))
    try: 
        p = Point(text)
        return float(p.latitude), float(p.longitude)
    except Exception: return None

def geocode_address(address: str, max_retries=3, delay=1) -> Optional[Tuple[float, float]]:
    for i in range(max_retries):
        try:
            loc = geolocator.geocode(address, timeout=10)
            if loc:
                return (loc.latitude, loc.longitude)
            return None
        except Exception:
            time.sleep(delay)
            delay *= 2
    return None
