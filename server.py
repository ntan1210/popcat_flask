from flask_cors import CORS
from flask import Flask, request, jsonify
import requests
import json
import threading
import time
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
CORS(app)

# Path to the JSON file to store click data
DATA_FILE = "click_data.json"


# Load data from JSON file or initialize an empty dictionary if file doesn't exist
def load_click_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# Save click data to JSON file
def save_click_data():
    with open(DATA_FILE, "w") as file:
        json.dump(click_data, file)


# Background function to save data to file every 5 seconds
def periodic_save():
    while True:
        save_click_data()
        time.sleep(5)


# Initialize click data
click_data = load_click_data()


# Get the user's country based on their IP
def get_country_by_ip(ip):
    try:
        response = requests.get(f"http://ipinfo.io/{ip}/json")
        data = response.json()
        return data.get("country", "Unknown")
    except Exception as e:
        print(f"Error getting country: {e}")
        return "Unknown"


@app.route("/track-click", methods=["POST"])
def track_click():
    ip_address = request.remote_addr
    country = get_country_by_ip(ip_address)

    if country not in click_data:
        click_data[country] = 0

    # Add click to the country's count
    click_data[country] += 1

    return jsonify(success=True, clicks=click_data[country])


@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    # Return the click leaderboard sorted by clicks
    leaderboard = sorted(click_data.items(), key=lambda x: x[1], reverse=True)
    return jsonify(leaderboard)


# Start background thread for periodic saving
save_thread = threading.Thread(target=periodic_save, daemon=True)
save_thread.start()

if __name__ == "__main__":
    app.run(debug=True)
