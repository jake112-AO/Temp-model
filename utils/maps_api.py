import os
import requests
from typing import Tuple
from urllib.parse import urlencode

API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")  # set in env

DEFAULT_TIMEOUT = 15

def fetch_google_satellite(lat: float, lon: float, zoom: int=18, size: Tuple[int,int]=(640,640)) -> bytes:
    if not API_KEY:
        assert False, "GOOGLE_MAPS_API_KEY not set"
    params = {
        "center": f"{lat},{lon}",
        "zoom": str(zoom),
        "size": f"{size[0]}x{size[1]}",
        "maptype": "satellite",
        "key": API_KEY,
    }
    url = "https://maps.googleapis.com/maps/api/staticmap?" + urlencode(params)
    r = requests.get(url, timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    return r.content

def fetch_google_streetview(lat: float, lon: float, heading: int=0, pitch: int=0, fov: int=90, size: Tuple[int,int]=(640,640)) -> bytes:
    if not API_KEY:
        assert False, "GOOGLE_MAPS_API_KEY not set"
    params = {
        "location": f"{lat},{lon}",
        "size": f"{size[0]}x{size[1]}",
        "heading": str(heading),
        "pitch": str(pitch),
        "fov": str(fov),
        "key": API_KEY,
    }
    url = "https://maps.googleapis.com/maps/api/streetview?" + urlencode(params)
    r = requests.get(url, timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    return r.content
