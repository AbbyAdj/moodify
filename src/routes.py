import os
from flask import render_template, request, url_for, redirect, abort, flash, Blueprint
from dotenv import load_dotenv
from src.utils.utils import (
    get_lat_and_lon,
    get_weather_data,
    get_playlist_link,
    get_spotify_token,
    generate_qr_code,
)

load_dotenv(verbose=True, override=True)

app_blueprint = Blueprint(name="moodify", import_name=__name__)

OPEN_WEATHER_MAP_API_KEY = os.environ["OPEN_WEATHER_MAP_API_KEY"]
SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]


@app_blueprint.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            return redirect(url_for("moodify.city_page", city=city))
        else:
            flash("Please enter a city...")
            return redirect(url_for("moodify.home"))
    return render_template("index.html")


@app_blueprint.route("/city/<city>", methods=["GET", "POST"])
def city_page(city):
    action = request.form.get("action")
    old_playlist_url = request.form.get("current_playlist_url", "")
    if request.method == "POST":
        if action == "new_city":
            new_city = request.form.get("city")
            if new_city and new_city.lower() != city.lower():
                return redirect(url_for("moodify.city_page", city=new_city))

    geocoding_info = get_lat_and_lon(api_key=OPEN_WEATHER_MAP_API_KEY, city=city)
    if not geocoding_info or not geocoding_info.get("lat"):
        return redirect(url_for("moodify.city_not_found", city=city))
    country = geocoding_info.get("country", None)
    weather_data = get_weather_data(
        api_key=OPEN_WEATHER_MAP_API_KEY, geocoding=geocoding_info
    )
    if not weather_data:
        abort(500)
    weather = weather_data["weather"]
    weather_icon_url = f"https://openweathermap.org/img/wn/{weather["icon"]}@2x.png"
    spotify_token = get_spotify_token(
        client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
    )
    playlist_url = get_playlist_link(weather=weather["main"], token=spotify_token)
    while playlist_url == old_playlist_url:
        playlist_url = get_playlist_link(weather=weather["main"], token=spotify_token)
    qr_code = generate_qr_code(playlist_url)
    return render_template(
        "index.html",
        weather=weather,
        city=city,
        country=country,
        weather_icon_url=weather_icon_url,
        playlist_url=playlist_url,
        qr_code=qr_code,
    )


@app_blueprint.route("/city_not_found")
def city_not_found():
    city = request.args.get("city", "unknown")
    return (
        render_template(
            "error.html",
            title="400 Error",
            subtitle="Oops! City Not Found",
            message=f"We couldn't find weather info for '{city}'. Try a different city.",
        ),
        400,
    )
