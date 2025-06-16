from src import app
from waitress import serve

if __name__ == "__main__":
    try:
        serve(app, host="0.0.0.0", port=8080)
    except Exception as e:
        print("ERROR:", e)
