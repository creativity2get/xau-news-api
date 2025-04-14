
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import os
import time

app = Flask(__name__)

@app.route('/news')
def scrape_bloomberg_calendar():
    url = "https://www.bloomberg.com/markets/economic-calendar"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return jsonify({"error": f"Status {response.status_code} from Bloomberg"}), 500

        soup = BeautifulSoup(response.content, "html.parser")
        events = []

        # Attempt to parse script type application/json or embedded JSON in <script> tags
        scripts = soup.find_all("script", type="application/json")
        for script in scripts:
            if 'economicCalendar' in script.text:
                events.append({"debug": "Found potential JSON but parsing not yet implemented."})
                break

        if not events:
            return jsonify({"debug": "No economic calendar data extracted from page"}), 200

        return jsonify(events)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
