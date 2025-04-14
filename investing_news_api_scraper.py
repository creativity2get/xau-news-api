
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime
import time

app = Flask(__name__)

@app.route('/news')
def fetch_investing_news():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://econcal.forexprostools.com/")
    time.sleep(10)  # Wait for full JS-rendering

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    table = soup.find("table")
    rows = table.find_all("tr") if table else []

    results = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 6:
            time_str = cols[0].text.strip()
            currency = cols[1].text.strip()
            impact = cols[2].get("title", "").strip().lower()
            event = cols[3].text.strip()
            forecast = cols[4].text.strip()
            actual = cols[5].text.strip()

            if "usd" in currency.lower() and "high" in impact:
                results.append({
                    "currency": currency,
                    "impact": impact,
                    "event": event,
                    "forecast": forecast,
                    "actual": actual,
                    "calendar_time": time_str
                })

    return jsonify(results)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
