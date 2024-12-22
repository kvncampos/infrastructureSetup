import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Load environment variables from .env
load_dotenv()

# Get WEB_ENV from environment
web_env = os.getenv("ENV", "development")

# Fetch message from environment variables
message = os.getenv("MESSAGE", "default")

# Configure Flask based on the environment
if web_env == "development":
    app.config["DEBUG"] = True
else:
    app.config["DEBUG"] = False


@app.route("/")
def index():
    visitor_ip = request.remote_addr  # Get the visitor's IP address
    return render_template("index.html", message=message, visitor_ip=visitor_ip)


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # Check the environment to determine the server to use
    is_production = os.getenv("FLASK_ENV") == "production"
    if is_production:
        # Use Gunicorn for production
        print("Running in production mode...")
    else:
        # Use Flask's development server
        print("Running in development mode...")
        app.run(host="0.0.0.0", port=5001, debug=app.config["DEBUG"])
