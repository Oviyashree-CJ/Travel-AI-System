import requests

def get_hotels(lat, lon):
    query = f"""
    [out:json];
    node["tourism"="hotel"](around:3000,{lat},{lon});
    out;
    """

    url = "https://overpass-api.de/api/interpreter"

    try:
        response = requests.post(url, data=query, timeout=30)

        if response.status_code != 200:
            print("Overpass error status:", response.status_code)
            return []

        if not response.text.strip():
            print("Overpass returned empty response")
            return []

        data = response.json()
        return data.get("elements", [])[:5]

    except Exception as e:
        print("Hotel agent error:", e)
        return []
