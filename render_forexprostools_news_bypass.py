
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/news')
def fetch_forexprost_news():
    url = "https://econcal.forexprostools.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.investing.com/",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data", "status": response.status_code}), 500

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        rows = table.find_all("tr") if table else []

        events = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 6:
                time_str = cols[0].text.strip()
                currency = cols[1].text.strip()
                impact_span = cols[2].find("span")
                impact = impact_span["title"] if impact_span else ""
                event = cols[3].text.strip()
                forecast = cols[4].text.strip()
                actual = cols[5].text.strip()

                if "USD" in currency and "High" in impact:
                    events.append({
                        "time": time_str,
                        "currency": currency,
                        "impact": impact,
                        "event": event,
                        "forecast": forecast,
                        "actual": actual
                    })

        return jsonify(events)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
