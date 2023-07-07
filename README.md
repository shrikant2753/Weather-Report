# Weather Report Application
The Weather Report application provides weather information using data fetched from the WeatherStack API. It allows users to retrieve current weather data for a specific location.

## Prerequisites
Make sure you have the following installed:
  - Python 3.x
  - Flask
  - pymongo

You can install Flask and pymongo by running the following commands:

```shell
pip install flask
pip install pymongo
```

## Configuration
To connect the application to MongoDB Atlas, follow these steps:

  1. Create a MongoDB Atlas cluster.
  2. Create a project and database in MongoDB Atlas.
  3. Create a collection named `weather_data` in the database.
  4. Obtain the connection string `(MONGO_URI)` from the MongoDB Atlas dashboard.
  
   Set the following values in the application:

* `MONGO_URI`: Replace `<username>`, `<password>`, `<cluster-url>`, and `<database-name>` with your MongoDB Atlas credentials and database details.

To access weather data, you need an API key from WeatherStack. Follow these steps to obtain the API key:

1. Create an account on WeatherStack.
2. Obtain your API key.
Set the following value in the application:

`api_key`: Replace `'your-api-key-from-weatherstack.com'` with your actual WeatherStack API key.

## Running the Application
To run the application, execute the following command:
```shell 
python main.py
```
The application will be accessible at `http://localhost:5000`.

## Usage
Once the application is running, you can access the following routes:

* **Home Page** : Access the home page at **`http://localhost:5000/`**.
* **Weather Report** : Fetch the weather report for a specific location by visiting **`http://localhost:5000/weather`**.

## Contributions
Contributions are welcome! If you have any suggestions, improvements, or new features to add, feel free to create a pull request.
