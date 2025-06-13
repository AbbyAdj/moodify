import base64
import io
import os
from pprint import pprint

import qrcode
from dotenv import load_dotenv
import requests

load_dotenv(verbose=True, override=True)

MOOD_THEMES = {
    "Clear": {"bg": "#ffeaa7", "text": "#2d3436"},
    "Clouds": {"bg": "#dfe6e9", "text": "#2d3436"},
    "Rain": {"bg": "#74b9ff", "text": "#2d3436"},
    "Snow": {"bg": "#ffffff", "text": "#2d3436"},
    "Thunderstorm": {"bg": "#636e72", "text": "#ffffff"},
    "Drizzle": {"bg": "#81ecec", "text": "#2d3436"},
    "Mist": {"bg": "#b2bec3", "text": "#2d3436"},
    "Fog": {"bg": "#b2bec3", "text": "#2d3436"},
    "Haze": {"bg": "#fab1a0", "text": "#2d3436"}
}

WEATHER_TO_MOOD = {
    "Clear": [
        "feel good",
        "happy vibes",
        "good vibes",
        "upbeat",
        "positive energy"
    ],
    "Clouds": [
        "lofi",
        "lofi hip hop",
        "chill lofi",
        "lofi beats",
        "study beats"
    ],
    "Rain": [
        "sad",
        "rainy day",
        "melancholy",
        "sad vibes",
        "heartbreak"
    ],
    "Snow": [
        "calm",
        "relaxing",
        "peaceful",
        "calm piano",
        "soft music"
    ],
    "Thunderstorm": [
        "intense",
        "workout",
        "power",
        "energetic",
        "pump up"
    ],
    "Drizzle": [
        "chill",
        "chill vibes",
        "relax",
        "cool down",
        "chill out"
    ],
    "Mist": [
        "ambient",
        "atmospheric",
        "space music",
        "background music",
        "meditative"
    ],
    "Fog": [
        "acoustic",
        "unplugged",
        "acoustic guitar",
        "acoustic session",
        "soft acoustic"
    ],
    "Haze": [
        "dream pop",
        "indie pop",
        "ethereal",
        "shoegaze",
        "ambient pop"
    ]
}

#########################
# TIME AND LOCATION API
#########################

def get_lat_and_lon(api_key: str, city: str)-> dict[str: int]:
    result = {}
    geocoding_endpoint = "http://api.openweathermap.org/geo/1.0/direct"
    query_params = {
        "q": city,
        "appid": api_key
    }
    try:
        response = requests.get(geocoding_endpoint, params=query_params)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            record = data[0]

            result = {
                "lat": record["lat"],
                "lon": record["lon"],
                "country": record["state"]
            }
        return result

    except Exception as e:
        return result

def get_weather_data(api_key: str, geocoding: dict, default_theme: dict | None =  None)-> dict[str: any]:
    result = {}
    query_params = {
        "lat": geocoding["lat"],
        "lon": geocoding["lon"],
        "appid": api_key
    }
    weather_endpoint = "https://api.openweathermap.org/data/2.5/weather"
    try:
        response = requests.get(weather_endpoint, params=query_params)
        response.raise_for_status()
        if response.status_code == 200 and geocoding:
            data = response.json()
            weather = data["weather"][0]
            theme = MOOD_THEMES.get(weather["main"], default_theme)
            result =  {
                "weather": weather,
                "theme": theme
            }
            return result
        else:
            return result

    except requests.exceptions.RequestException as e:
        pass

# NOT NEEDED FOR NOW!
def get_current_time(geocoding):
    query_params = {
        "latitude": geocoding["lat"],
        "longitude": geocoding["lon"]
    }
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
# SPOTIFY API
#########################

def get_spotify_token(client_id, client_secret):
    spotify_endpoint = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(
        url=spotify_endpoint,
        data={
            "grant_type": "client_credentials"
        },
        auth=(client_id, client_secret)
    )
    access_token = auth_response.json()["access_token"]
    return access_token

def get_playlist_link(weather, token):
    moods = WEATHER_TO_MOOD[weather]
    for mood in moods:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            params = {
                "q": mood,
                "type": "playlist",
                "limit": 1
            }
            spotify_endpoint = "https://api.spotify.com/v1/search"
            response = requests.get(
                url=spotify_endpoint,
                headers=headers,
                params=params)
            data = response.json()
            items = data["playlists"]["items"]
            if items[0]:
                pprint(data)
                return items[0]['external_urls']['spotify']
        except Exception as e:
            return None
    fallback_playlist = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"  # Spotify's "Today's Top Hits"
    return fallback_playlist

def generate_qr_code(playlist_url):
    qr_code = qrcode.make(playlist_url)
    buffer = io.BytesIO()
    qr_code.save(buffer, format="PNG")
    buffer.seek(0)
    img_data = base64.b64encode(buffer.read()).decode('utf-8')
    return f"data:image/png;base64,{img_data}"

if __name__ == "__main__":
    SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
    SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
    spotify_token = get_spotify_token(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
    playlist_url_ = get_playlist_link(weather="Clear", token=spotify_token)




