# Moodify 🎵☁️

Moodify is a Flask web app that creates Spotify playlists based on the current weather in your city. It uses real-time weather data to suggest music that matches the mood of the skies.

## Features

- Fetches live weather data using the OpenWeatherMap API
- Generates a Spotify playlist based on weather conditions
- Displays matching weather icons
- Clean, responsive UI using Bootstrap
- QR code generation for sharing playlists

## Live Demo

You can try the app here: [moodify](https://moodify-pq9d.onrender.com)


## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/AbbyAdj/moodify.git
   cd moodify
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the root directory and add the following:

   ```
   OPENWEATHERMAP_API_KEY=your_api_key_here
   SPOTIFY_CLIENT_ID=your_client_id_here
   SPOTIFY_CLIENT_SECRET=your_client_secret_here
   ```

5. **Run the app**
   ```bash
   flask run
   ```

   Then open `http://localhost:5000` in your browser.

## Tech Stack

- **Backend**: Python, Flask
- **APIs**: OpenWeatherMap, Spotify
- **Frontend**: HTML, CSS (Bootstrap), Javascript, Jinja2
- **Other**: `requests`, `python-dotenv`, `base64` (for QR codes)

## Coming Soon
    
- Custom playlist moods
- Location saving
- Light/dark theme toggle

## Contribution

Contributions and suggestions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
Built by [Abby Adjei](https://github.com/AbbyAdj).
For feedback or collaboration, reach out via [GitHub](https://github.com/AbbyAdj) or [LinkedIn](https://www.linkedin.com/in/abigailadjeia/) 
