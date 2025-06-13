import os
from flask import Flask, render_template_string, request
import requests
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)

app = Flask(__name__)

OPEN_WEATHER_MAP_API_KEY = os.environ["OPEN_WEATHER_MAP_API_KEY"]

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