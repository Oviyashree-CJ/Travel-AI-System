from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests

from nlp_parser import extract_destination
from agents.flight_agent import get_flights
from agents.hotel_agent import get_hotels
from agents.guide_agent import get_places
from agents.restaurant_agent import get_restaurants

load_dotenv()

app = Flask(__name__)

def geocode_city(city):
    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        "q": city,
        "key": os.getenv("OPENCAGE_API_KEY"),
        "limit": 1
    }

    try:
        res = requests.get(url, params=params, timeout=10).json()

        # ✅ SAFE CHECK
        if not res.get("results"):
            print(f"[WARN] No geocoding result for: {city}")
            return None, None

        geo = res["results"][0]["geometry"]
        return geo["lat"], geo["lng"]

    except Exception as e:
        print("[ERROR] Geocoding failed:", e)
        return None, None


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        user_input = request.form["query"]
        destination = extract_destination(user_input)

        if destination:
            lat, lon = geocode_city(destination)

            if lat is None or lon is None:
                return render_template(
                    "index.html",
                    result={"error": f"Could not find location for '{destination}'"}
                )


            result = {
                "destination": destination,
                "lat": lat,
                "lon": lon,
                "flights": get_flights(destination),
                "hotels": get_hotels(lat, lon),
                "places": get_places(lat, lon),
                "restaurant": get_restaurants(lat, lon)
            }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
