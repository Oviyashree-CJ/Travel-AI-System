import requests

def get_places(lat, lon):
    """
    Fetch famous tourist attractions near a location using Overpass API
    """
    query = f"""
    [out:json];
    (
      node["tourism"="attraction"](around:5000,{lat},{lon});
      node["historic"](around:5000,{lat},{lon});
      node["amenity"="place_of_worship"](around:5000,{lat},{lon});
      node["leisure"="park"](around:5000,{lat},{lon});
    );
    out;
    """

    url = "https://overpass-api.de/api/interpreter"

    try:
        response = requests.post(url, data=query, timeout=30)

        if response.status_code != 200 or not response.text.strip():
            return fallback_places()

        data = response.json()
        places = []

        for el in data.get("elements", []):
            name = el.get("tags", {}).get("name")
            if name:
                places.append(name)

        return places[:6] if places else fallback_places()

    except Exception:
        return fallback_places()


def fallback_places():
    return [
        "Major historical landmark",
        "Popular cultural attraction",
        "Famous city location"
    ]
