import os
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
from src.utils import get_lat_and_lon, get_weather_data, get_playlist_link, get_spotify_token, generate_qr_code

load_dotenv(verbose=True, override=True)

app = Flask(__name__)

OPEN_WEATHER_MAP_API_KEY = os.environ["OPEN_WEATHER_MAP_API_KEY"]
SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]


@app.route("/", methods=["GET", "POST"])
def home():
    # city = ""
    # country = ""
    # theme = {"bg": "#F5F5DC", "text": "#2d3436"}  # default theme to use incase
    if request.method == "POST":
        city = request.form.get("city")
        country = request.form.get("country")

        if city:
            geocoding_info = get_lat_and_lon(api_key=OPEN_WEATHER_MAP_API_KEY, city=city)
            weather_data = get_weather_data(api_key=OPEN_WEATHER_MAP_API_KEY, geocoding=geocoding_info)
            weather = weather_data["weather"]
            weather_icon_url =  f"https://openweathermap.org/img/wn/{weather["icon"]}@2x.png"
            # theme = weather_data["theme"]
            spotify_token = get_spotify_token(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
            playlist_url = get_playlist_link(weather=weather["main"], token=spotify_token)
            qr_code = generate_qr_code(playlist_url)

            return render_template(
                "index.html",
                weather=weather,
                city=city,
                country= geocoding_info["country"],
                weather_icon_url=weather_icon_url,
                # theme=theme,
                playlist_url=playlist_url,
                qr_code=qr_code
                )
    return None # TODO: raise exception or error message

if __name__ == "__main__":
    app.run(debug=True)

