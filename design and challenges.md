# Design
1. The Weather Report application is built using the Flask framework, which provides a simple and lightweight way to develop web applications in Python.
2. The application follows a client-server architecture, where the server-side is implemented using Flask and the client-side is rendered using HTML templates.
3. MongoDB Atlas is used as the database to store weather data retrieved from the WeatherStack API. MongoDB offers a flexible and scalable solution for storing and querying data.
4. The application consists of different routes that handle specific functionalities, such as fetching weather data, displaying data, and filtering data based on user input.
5. HTML templates are used to render the weather data and provide a user-friendly interface for accessing and interacting with the application.


# Challenges Faced
* Connecting Flask with MongoDB: Setting up the connection between Flask and MongoDB required configuring the MongoDB Atlas connection string and handling any connection errors that occurred during the process. Ensuring the connection was established successfully was a challenge.
* Handling API Requests: Implementing the logic to handle different types of API requests, such as fetching weather data by latitude and longitude or by city name, required careful validation and constructing the API request parameters correctly.
* Formatting and Displaying Data: Representing the retrieved weather data in a suitable format for display in HTML templates posed a challenge. Determining which data fields to show and how to format them to provide a clear and concise view for users required careful consideration.
* Error Handling: Implementing proper error handling and displaying meaningful error messages to users in case of failures or invalid data input was important for providing a smooth user experience. Ensuring all possible error scenarios were covered and handled appropriately was a challenge.
