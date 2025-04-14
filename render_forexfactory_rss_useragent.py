
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import time
import os

app = Flask(__name__)

@app.route('/news')
def get_forexfactory_news():
    url = "https://www.forexfactory.com/ff_calendar_thisweek.xml"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return jsonify({"error": f"RSS Feed returned status {response.status_code}"}), 500

        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("event")

        news = []
        for item in items:
            try:
                currency = item.currency.text
                event = item.title.text
                impact = item.impact.text.lower()
                forecast = item.forecast.text if item.forecast else ""
                actual = item.actual.text if item.actual else ""
                previous = item.previous.text if item.previous else ""
                date = item.date.text
                time_ = item.time.text

                if "usd" not in currency.lower():
                    continue

                news.append({
                    "currency": currency,
                    "event": event,
                    "impact": impact,
                    "forecast": forecast,
                    "actual": actual,
                    "previous": previous,
                    "date": date,
                    "time": time_,
                    "timestamp": int(time.time())
                })
            except Exception:
                continue

        if not news:
            return jsonify({"debug": "Parsed feed, but no USD events found."}), 200

        return jsonify(news)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
