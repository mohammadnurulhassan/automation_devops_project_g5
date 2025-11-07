import datetime as dt
import requests
from flask import Flask, render_template
from src.api_call import get_coordinates, get_current_weather, get_historical_weather

app = Flask(__name__)

@app.route("/")
def index():
    lat, lon = get_coordinates("Stockholm")

    now = get_current_weather(lat, lon)
    page_data = {
        "temperature_c": int(now["main"]["temp"]),  
        "weather": now["weather"][0]["description"].capitalize(),
        "time": dt.datetime.now().strftime("%B, %d - %Y"),
    }

    last_year_data = None
    try:
        target = (
            dt.datetime.now(dt.timezone.utc)
            .replace(hour=12, minute=0, second=0, microsecond=0)
            - dt.timedelta(days=365)
        )

        hist = get_historical_weather(lat, lon, target)

        if "data" in hist:
            payload = hist["data"][0]
        else:
            payload = hist.get("current")

        if payload:
            last_year_data = {
                "temperature_c": int(payload["temp"]),  
                "weather": payload["weather"][0]["description"].capitalize(),
                "date": target.strftime("%B, %d - %Y"),
            }

    except requests.HTTPError as e:
        print("History API failed:", e)
    except Exception as e:
        print("History API error:", e)

    return render_template("index.html", page_data=page_data, last_year_data=last_year_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
