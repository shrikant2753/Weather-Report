from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from bson import ObjectId
import requests

import json


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


app = Flask(__name__)
app.json_encoder = JSONEncoder

# MongoDB Atlas configuration
MONGO_URI = 'mongodb+srv://shrikantrp00:shrikant@cluster0.2uzxml0.mongodb.net/weather_db?retryWrites=true&w=majority'

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client.weather_db
collection = db.weather_data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def weather_fetch():
    api_key = 'dbd216b087d720fa176b2d4620263dc1'
    latitude = request.form['lat']
    longitude = request.form['lon']
    city = request.form['city']

    if latitude and longitude:
        base_url = 'http://api.weatherstack.com/current'
        params = {
            'access_key': api_key,
            'query': f'{latitude},{longitude}'
        }
    elif city:
        base_url = 'http://api.weatherstack.com/current'
        params = {
            'access_key': api_key,
            'query': city
        }
    else:
        return jsonify({'error': 'Latitude and longitude or city name are required'}), 400

    try:
        # Make the API request
        response = requests.get(base_url, params=params)
        result = response.json()

        # Check if the API request was successful
        if response.status_code == 200:
            # Check if the weather data is valid
            if 'current' in result:
                # Store the weather data in MongoDB
                collection.insert_one(result)

                # Pass the weather data to the template
                return render_template('response.html', result=result)
            else:
                return jsonify({'error': 'Invalid weather data'}), 400
        else:
            return jsonify({'error': 'Failed to fetch weather data'}), response.status_code
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)

