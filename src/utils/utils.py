import base64
import io
import os
import random
from pprint import pprint
import qrcode
from dotenv import load_dotenv
import requests

load_dotenv(verbose=True, override=True)


WEATHER_TO_MOOD = {
    "Clear": ["feel good", "happy vibes", "good vibes", "upbeat", "positive energy"],
    "Clouds": ["lofi", "lofi hip hop", "chill lofi", "lofi beats", "study beats"],
    "Rain": ["sad", "rainy day", "melancholy", "sad vibes", "heartbreak"],
    "Snow": ["calm", "relaxing", "peaceful", "calm piano", "soft music"],
    "Thunderstorm": ["intense", "workout", "power", "energetic", "pump up"],
    "Drizzle": ["chill", "chill vibes", "relax", "cool down", "chill out"],
    "Mist": ["ambient", "atmospheric", "space music", "background music", "meditative"],
    "Fog": [
        "acoustic",
        "unplugged",
        "acoustic guitar",
        "acoustic session",
        "soft acoustic",
    ],
    "Haze": ["dream pop", "indie pop", "ethereal", "shoegaze", "ambient pop"],
}

#########################
# TIME AND LOCATION UTILS
#########################


def get_lat_and_lon(api_key: str, city: str) -> dict[str:int]:

    result = {}
    geocoding_endpoint = "http://api.openweathermap.org/geo/1.0/direct"
    query_params = {"q": city, "appid": api_key}
    try:
        response = requests.get(geocoding_endpoint, params=query_params)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            record = data[0]

            result = {
                "lat": record["lat"],
                "lon": record["lon"],
                "country": record.get("state", ""),
            }
        return result

    except Exception as e:
        return None


def get_weather_data(
    api_key: str, geocoding: dict, default_theme: dict | None = None
) -> dict[str:any]:

    weather_endpoint = "https://api.openweathermap.org/data/2.5/weather"
    try:
        if geocoding:
            query_params = {
                "lat": geocoding["lat"],
                "lon": geocoding["lon"],
                "appid": api_key,
            }
            response = requests.get(weather_endpoint, params=query_params)
            response.raise_for_status()
            if response.status_code == 200:
                data = response.json()
                weather = data["weather"][0]
                result = {"weather": weather}
                return result
            else:
                return {}
        else:
            return {}

    except requests.exceptions.RequestException as e:
        return None


# NOT NEEDED FOR NOW!
def get_current_time(geocoding):
    query_params = {"latitude": geocoding["lat"], "longitude": geocoding["lon"]}
    endpoint = "https://timeapi.io/api/timezone/coordinate"
    try:
        response = requests.get(endpoint, params=query_params)
        response.raise_for_status()
        if response.status_code == 200 and geocoding:
            data = response.json()
            local_time = data["currentLocalTime"]
            current_hour = local_time[11:13]
        return None
    except requests.exceptions.RequestException as e:
        return None


#########################
# SPOTIFY UTILS
#########################


def get_spotify_token(client_id, client_secret):
    spotify_endpoint = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(
        url=spotify_endpoint,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )
    access_token = auth_response.json()["access_token"]
    return access_token


def get_playlist_link(weather, token):
    spotify_endpoint = "https://api.spotify.com/v1/search"
    fallback_playlist_url = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"  # Spotify's "Today's Top Hits"
    moods = WEATHER_TO_MOOD[weather]
    random.shuffle(moods)

    for mood in moods:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            query_params = {"q": mood, "type": "playlist", "limit": 10}
            response = requests.get(
                url=spotify_endpoint, headers=headers, params=query_params
            )
            data = response.json()
            items = data["playlists"]["items"]
            if items:
                valid_items = [item for item in items if item]
                # pprint(valid_items)
                chosen_playlist = random.choice(valid_items)
                playlist_url = chosen_playlist["external_urls"]["spotify"]
                return playlist_url
        except Exception as e:
            return None
    else:
        return fallback_playlist_url

    return fallback_playlist_url


def generate_qr_code(playlist_url):
    qr_code = qrcode.make(playlist_url)
    buffer = io.BytesIO()
    qr_code.save(buffer, format="PNG")
    buffer.seek(0)
    img_data = base64.b64encode(buffer.read()).decode("utf-8")
    return f"data:image/png;base64,{img_data}"


if __name__ == "__main__":
    SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
    SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
    spotify_token = get_spotify_token(
        client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
    )
    playlist_url_ = get_playlist_link(weather="Clouds", token=spotify_token)
