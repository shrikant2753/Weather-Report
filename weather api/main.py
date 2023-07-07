from datetime import datetime
from flask import Flask, request, render_template
from pymongo import MongoClient
import requests

app = Flask(__name__)

# MongoDB Atlas configuration
# MONGO_URI = 'mongodb+srv://<username>:<password>@<cluster-url>/<database-name>?retryWrites=true&w=majority'
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
    # api_key = 'your api key of weatherstack.com'
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
        return f'<p>error : Latitude and longitude or city name are required</p>', 400

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

                # Extract current and location fields from the result
                data = {
                    'current': result['current'],
                    'location': result['location']
                }

                # Pass the weather data to the template
                return render_template('response.html', result=data)
            else:
                return f'<p>error : Invalid weather data</p>', 400
        else:
            return f'<p>error : Failed to fetch weather data</p>', response.status_code
    except requests.RequestException as e:
        error_message = str(e)
        return f'<p>Error: {error_message}</p>', 500


@app.route('/weather-data', methods=['GET'])
def get_weather_data():
    try:
        # Retrieve all weather data from MongoDB collection
        weather_data = list(collection.find())

        # Format the weather data
        formatted_data = []
        for data in weather_data:
            formatted_data.append(format_data(data))

        # Render the weather data using an HTML template
        return render_template('weather_data.html', result=formatted_data)

    except Exception as e:
        # Handle the exception and return an appropriate response
        error_message = str(e)
        return f'<p>Error: {error_message}</p>', 500


@app.route('/weather-data-for-city', methods=['GET'])
def get_weather_data_for_city():
    try:
        # Get query parameter
        city = request.args.get('city')

        # Build aggregation pipeline
        pipeline = [
            {"$match": {"location.name": city}},
            {"$group": {
                "_id": None,
                "average_temperature": {"$avg": "$current.temperature"},
                "max_temperature": {"$max": "$current.temperature"},
                "min_temperature": {"$min": "$current.temperature"}
            }}
        ]

        # Execute the aggregation query
        result = list(collection.aggregate(pipeline))

        # Check if the result is not empty
        if result:
            stats = result[0]  # Get the statistical information
            return render_template('weather_data_for_city.html', result=stats, name=city)
        else:
            return f'<p>Error: No weather data found for the city</p>', 404

    except Exception as e:
        error_message = str(e)
        return f'<p>Error: {error_message}</p>', 500


@app.route('/weather-data_filter', methods=['GET'])
def get_weather_data_filter():
    try:
        # Extract query parameters
        location = request.args.get('city')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        min_temperature = request.args.get('min_temperature')
        max_temperature = request.args.get('max_temperature')

        # Construct the query filter based on the provided parameters
        query_filter = {}

        if location:
            query_filter['location.name'] = location

        if start_date and end_date:
            start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
            query_filter['current.observation_time'] = {
                '$gte': start_datetime,
                '$lte': end_datetime
            }

        if min_temperature:
            query_filter['current.temperature'] = {'$gte': float(min_temperature)}

        if max_temperature:
            query_filter['current.temperature'] = {'$lte': float(max_temperature)}

        # Retrieve filtered weather data from MongoDB collection
        weather_data = list(collection.find(query_filter))
        if weather_data is None:
            return'No data found for %s' %location
        
        formatted_data = []
        for data in weather_data:
            formatted_data.append(format_data(data))

        # Render the weather data using an HTML template
        return render_template('weather_data.html', result=formatted_data)

    except Exception as e:
        error_message = str(e)
        return f'<p>Error: {error_message}</p>', 500


def format_data(data):
    formated_data = { 
                      'City':data['location']['name'],
                      'Country':data['location']['country'],
                      'Region':data['location']['region'],
                      'Latitude':data['location']['lat'],
                      'Longitude':data['location']['lon'],
                      'Local time':data['location']['localtime'],
                      'Observation_time':data['current']['observation_time'],
                      'Temperature':data['current']['temperature'],
                      'Wind speed':data['current']['wind_speed'],
                      'Wind direction':data['current']['wind_dir'],
                      'Atmospheric pressure':data['current']['pressure'],
                      'Humidity':data['current']['humidity'],
                      'Cloudcover':data['current']['cloudcover'],
                      'Visibility':data['current']['visibility'],
                      'UV index':data['current']['uv_index']
                    }
    return formated_data


if __name__ == '__main__':
    app.run(debug=True)
