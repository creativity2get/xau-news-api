
# render_myfxbook_api.py — FINAL VERSION FOR RENDER.COM

from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import time
import os

app = Flask(__name__)

@app.route('/news')
def get_news():
    url = "https://www.myfxbook.com/forex-economic-calendar"
    try:
        page = requests.get(url, timeout=10)
        soup = BeautifulSoup(page.text, 'html.parser')
        rows = soup.select('tr.calendarRow')
        news_list = []

        for row in rows:
            try:
                currency = row.select_one('.calendarCurrency').text.strip()
                event = row.select_one('.calendarEvent').text.strip()
                impact_icon = row.select_one('.calendarImpact i')
                impact = impact_icon['title'].strip().lower() if impact_icon else "low"
                actual = row.select_one('.calendarActual').text.strip()
                forecast = row.select_one('.calendarForecast').text.strip()

                if 'usd' not in currency.lower():
                    continue
                if not actual or not forecast or actual == '-' or forecast == '-':
                    continue

                news_list.append({
                    'currency': currency,
                    'event': event,
                    'impact': impact,
                    'actual': actual.replace('%',''),
                    'forecast': forecast.replace('%',''),
                    'timestamp': int(time.time())
                })
            except Exception:
                continue

        return jsonify(news_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
