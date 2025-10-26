import io
from PIL import Image
from coord_utils import parse_latlon, geocode_address
from maps_api import fetch_google_satellite, fetch_google_streetview

def get_images_for_location(location_str, headings=(0,90,180,270)):
    coords = parse_latlon(location_str) or geocode_address(location_str)
    if not coords:
        raise ValueError("Location parse failed")
    lat, lon = coords
    imgs = {}
    imgs['satellite'] = Image.open(io.BytesIO(fetch_google_satellite(lat, lon)))
    imgs['street_views'] = []
    for h in headings:
        try:
            imgs['street_views'].append(Image.open(io.BytesIO(fetch_google_streetview(lat, lon, heading=h))))
        except Exception as e: # Street view may not exist, so we log + skip
            continue
    return lat, lon, imgs

def analyze_and_store(location_str, vision_system, vector_db, metadata=None):
    lat, lon, imgs = get_images_for_location(location_str)
    # Convert images to the format your model expects. Example: bytes or PIL.
    score, evidence = vision_system.score_images(imgs)  # TODO
    embeddings = vision_system.embed(evidence)  # TODO
    vector_db.upsert({
        "id": f"{lat}_{lon}",
        "embedding": embeddings,
        "metadata": {
            "lat": lat, "lon": lon, "source": "google_maps", **(metadata or {})
        }
    })
    return {"score": score, "evidence": evidence}
