
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import time
import os

app = Flask(__name__)

@app.route('/news')
def get_news():
    url = "https://www.investing.com/economic-calendar/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    try:
        page = requests.get(url, headers=headers, timeout=10)
        if page.status_code != 200:
            return jsonify({"error": f"Status {page.status_code} from Investing.com"}), 500

        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.find("table", {"id": "economicCalendarData"})
        if not table:
            return jsonify({"debug": "Calendar table not found"}), 200

        rows = table.select("tr.js-event-item")
        if not rows:
            return jsonify({"debug": "No economic event rows found"}), 200

        news = []
        for row in rows:
            try:
                time_str = row.get("data-event-datetime", "").strip()
                currency = row.get("data-event-currency", "").strip()
                impact = row.get("data-event-importance", "").strip()
                actual = row.get("data-event-actual", "").strip()
                forecast = row.get("data-event-forecast", "").strip()
                previous = row.get("data-event-previous", "").strip()
                event_name = row.find("td", class_="event").text.strip()

                if "USD" not in currency:
                    continue
                if impact != "3":  # Only high-impact
                    continue

                news.append({
                    "currency": currency,
                    "event": event_name,
                    "actual": actual,
                    "forecast": forecast,
                    "previous": previous,
                    "impact": "high",
                    "time": time_str,
                    "timestamp": int(time.time())
                })
            except Exception:
                continue

        if not news:
            return jsonify({"debug": "USD events filtered out or no high impact"}), 200

        return jsonify(news)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
