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
    total_clicks += 1
    return jsonify({"clicks": total_clicks})


# Start the auto increment on server startup
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
