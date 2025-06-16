import base64
import pytest
from unittest.mock import patch, Mock
from requests.exceptions import RequestException
from src.utils.utils import (
    get_lat_and_lon,
    get_weather_data,
    get_current_time,
    get_spotify_token,
    get_playlist_link,
    generate_qr_code,
    WEATHER_TO_MOOD,
)

# NOTE: Not testing get current time for now as it is not being used

#########################
# TIME AND LOCATION UTILS
#########################


# @pytest.mark.skip
class TestGetLatAndLon:

    @patch("src.utils.utils.requests.get")
    def test_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"lat": 12.34, "lon": 56.78, "state": "TestCountry"}
        ]
        mock_get.return_value = mock_response

        result = get_lat_and_lon("fake_api_key", "TestCity")
        assert result == {"lat": 12.34, "lon": 56.78, "country": "TestCountry"}
        mock_get.assert_called_once()

    @patch("src.utils.utils.requests.get")
    def test_success_and_no_country(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"lat": 1.23, "lon": 4.56}]
        mock_get.return_value = mock_response

        result = get_lat_and_lon("fake_api_key", "NoStateCity")
        assert result == {"lat": 1.23, "lon": 4.56, "country": ""}
        mock_get.assert_called_once()

    @patch("src.utils.utils.requests.get")
    def test_failure(self, mock_get):
        mock_get.side_effect = Exception("API error")
        result = get_lat_and_lon("fake_api_key", "FailCity")
        assert result is None


# @pytest.mark.skip
class TestGetWeatherData:
    @patch("src.utils.utils.requests.get")
    def test_returns_data_if_200_success_and_geocodes(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "weather": [{"main": "Clear", "description": "clear sky"}]
        }
        mock_get.return_value = mock_response

        geocoding = {"lat": 12.34, "lon": 56.78}
        result = get_weather_data("fake_api_key", geocoding)
        assert result == {"weather": {"main": "Clear", "description": "clear sky"}}

    @patch("src.utils.utils.requests.get")
    def test_returns_empty_dict_for_200_or_no_geocodes(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 300
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        geocoding = {"lat": 12.34, "lon": 56.78}
        no_geocoding = {}
        result_bad_response = get_weather_data("fake_api_key", geocoding)

        mock_response.status_code = 200
        result_no_geocoding = get_weather_data("fake_api_key", no_geocoding)

        assert result_no_geocoding == result_bad_response == {}

    @patch("src.utils.utils.requests.get")
    def test_get_weather_data_failure(self, mock_get):
        mock_get.side_effect = RequestException("API error")
        geocoding = {"lat": 12.34, "lon": 56.78}
        result = get_weather_data("fake_api_key", geocoding)
        assert result is None


#########################
# SPOTIFY UTILS
#########################


# @pytest.mark.skip
class TestGetSpotifyToken:
    @patch("src.utils.utils.requests.post")
    def test_get_spotify_token_success(self, mock_post: Mock):
        mock_response = Mock()
        mock_response.json.return_value = {"access_token": "test_token"}
        mock_post.return_value = mock_response

        token = get_spotify_token("fake_id", "fake_secret")
        assert token == "test_token"
        mock_post.assert_called_once_with(
            url="https://accounts.spotify.com/api/token",
            data={"grant_type": "client_credentials"},
            auth=("fake_id", "fake_secret"),
        )

    @patch("src.utils.utils.requests.post")
    def test_get_spotify_token_failure(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("API error")
        mock_post.return_value = mock_response

        with pytest.raises(Exception):
            get_spotify_token("fake_id", "fake_secret")


# @pytest.mark.skip
class TestGetPlaylistLink:
    @patch("src.utils.utils.requests.get")
    def test_returns_playlist_url_on_success(self, mock_get: Mock):
        mock_response = Mock()
        mock_response.json.return_value = {
            "playlists": {
                "items": [
                    {
                        "external_urls": {
                            "spotify": "https://open.spotify.com/playlist/123"
                        }
                    }
                ]
            }
        }
        mock_get.return_value = mock_response

        token = "fake_token"
        url = get_playlist_link("Clear", token)
        assert url == "https://open.spotify.com/playlist/123"
        mock_get.assert_called()

    @patch("src.utils.utils.requests.get")
    @patch("src.utils.utils.WEATHER_TO_MOOD", {"Clear": ["feel good"]})
    def test_returns_fallback_playlist_url_if_no_items_for_one_mood(
        self, mock_get: Mock
    ):
        mock_response = Mock()
        mock_response.json.return_value = {"playlists": {"items": []}}
        mock_get.side_effect = [mock_response]

        token = "fake_token"
        url = get_playlist_link("Clear", token)
        assert url == "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"

    @patch("src.utils.utils.requests.get")
    @patch("src.utils.utils.WEATHER_TO_MOOD", {"Clear": ["feel good", "happy vibes"]})
    def test_returns_fallback_playlist_url_if_no_items_for_more_than_one_mood(
        self, mock_get: Mock
    ):
        mock_response = Mock()
        mock_response.json.return_value = {"playlists": {"items": []}}
        mock_get.side_effect = [mock_response, mock_response]

        token = "fake_token"
        url = get_playlist_link("Clear", token)
        assert url == "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
        assert mock_get.call_count == 2

    @patch("src.utils.utils.requests.get")
    def test_returns_none_on_exception(self, mock_get: Mock):
        mock_get.side_effect = Exception("API error")
        token = "fake_token"
        url = get_playlist_link("Clear", token)
        assert url is None


# @pytest.mark.skip
class TestGenerateQRCode:
    def test_returns_base64_png_data_uri(self):
        playlist_url = "https://open.spotify.com/playlist/123"
        result = generate_qr_code(playlist_url)
        assert isinstance(result, str)
        assert result.startswith("data:image/png;base64,")

        # Check that the base64 part decodes without error

        base64_data = result.split(",", 1)[1]
        decoded = base64.b64decode(base64_data)
        assert decoded[:8] == b"\x89PNG\r\n\x1a\n"  # PNG file signature
