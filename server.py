from flask_cors import CORS
from flask import Flask, request, jsonify
import requests
import json
import threading
import time
from werkzeug.middleware.proxy_fix import ProxyFix
from threading import Timer
import random

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
CORS(app)

# Global click counter
total_clicks = 0


# Endpoint to get the current click count
@app.route("/api/clicks", methods=["GET"])
def get_clicks():
    global total_clicks
    return jsonify({"clicks": total_clicks})


# Endpoint to handle user click
@app.route("/api/click", methods=["POST"])
def add_click():
    global total_clicks
    random_increment = random.randint(1, 10)  # Random increment between 1 and 10
    total_clicks += random_increment
    return jsonify({"clicks": total_clicks})


# Function to increment clicks automatically every 20 seconds
def auto_increment():
    global total_clicks
    random_increment = random.randint(1, 10)  # Random increment between 1 and 10
    total_clicks += random_increment
    print(f"Auto-incremented by {random_increment}, total clicks: {total_clicks}")
    # Schedule the function to run again after 20 seconds
    Timer(20, auto_increment).start()


# Start the auto increment on server startup
if __name__ == "__main__":
    auto_increment()
    app.run(host="0.0.0.0", port=8000, debug=True)
