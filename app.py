from flask import Flask
from scrape import scrapePirates, scrapeWeather
import json
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World."
@app.route('/scrapeweather', methods=['GET'])
def scrape_weather():
    #scrape weather call
    weather_data_path ='https://raw.githubusercontent.com/qillbel/scrap1_q-wmo/main/scraped_weather.csv'
    got_df = pd.read_csv(weather_data_path)
    result = got_df.to_json(orient='records')
    parsed = json.loads(result)
    resu = json.dumps(parsed)
    return resu

@app.route('/hometest')
def home():
    return "Home page test"

if __name__ == "__main__":
    app.run()