
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/news')
def fetch_usd_news():
    url = "https://econcal.forexprostools.com/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data", "status": response.status_code}), 500

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr") if table else []

    results = []
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
                results.append({
                    "time": time_str,
                    "currency": currency,
                    "impact": impact,
                    "event": event,
                    "forecast": forecast,
                    "actual": actual
                })

    return jsonify(results)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
