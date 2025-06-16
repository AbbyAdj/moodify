from unittest.mock import patch

import pytest
from flask import Flask
from src.routes import app_blueprint
from pprint import pprint


class TestHomeRoute:
    def test_home_get(self, test_client):
        response = test_client.get("/")

        assert response.status_code == 200
        assert b"Get Another Playlist" not in response.data
        assert (
            b'<input type="text" name="city" placeholder="Enter your city..." value="">'
            in response.data
        )

    def test_home_post_with_city_redirected(self, test_client):
        response = test_client.post("/", data={"city": "London"})

        assert response.status_code == 302  # redirection
        assert "/city/London" in response.headers["Location"]
        # location cause of the redirection, it shows the url client was redirected to

    def test_home_post_without_city(self, test_client):
        response = test_client.post("/", data={"city": ""}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Please enter a city" in response.data  # Check that flash shows


class TestCityPageRoute:
    def test_home_post_with_city_end_html(self, test_client):
        with patch(
            "src.routes.get_lat_and_lon",
            return_value={"lat": 51.5, "lon": -0.1, "country": "England"},
        ), patch(
            "src.routes.get_weather_data",
            return_value={
                "weather": {
                    "main": "Cloudy",
                    "icon": "03d",
                    "description": "cloudy weather",
                }
            },
        ), patch(
            "src.routes.get_spotify_token", return_value="fake_token"
        ), patch(
            "src.routes.get_playlist_link", return_value="http://playlist.url"
        ), patch(
            "src.routes.generate_qr_code", return_value="fake_qr_code"
        ):

            response = test_client.get("/city/London")
            assert response.status_code == 200
            assert b"The weather in London, England is cloudy weather" in response.data
            assert b"http://playlist.url" in response.data

        assert response.status_code == 200


class TestErrorHandling:
    def test_city_route_invalid_city(self, test_client):
        with patch("src.routes.get_lat_and_lon", return_value=None):
            response = test_client.get("/city/InvalidCity", follow_redirects=True)

            assert response.status_code == 400
            assert b"City Not Found" in response.data
            assert (
                b"We couldn&#39;t find weather info for &#39;InvalidCity&#39;. Try a different city."
                in response.data
            )

    def test_404_error(self, test_client):
        response = test_client.get("/nonexistentpage")
        pprint(response.data)
        assert response.status_code == 404
        assert b"Page Not Found" in response.data

    def test_500_error(self, test_client):
        with patch("src.routes.get_weather_data") as mock_weather_data:
            mock_weather_data.return_value = None
            response = test_client.get("/city/London")
            assert response.status_code == 500
            assert (
                b"Something went wrong on our end. Please try again later."
                in response.data
            )
