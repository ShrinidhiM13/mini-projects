import requests
from flask import Flask, request, render_template

app = Flask(__name__)

# Function to get weather data using OpenWeather One Call API 3.0
def get_weather(city):
    api_key = "06dffbeb7c0c4a146315d3323ac03c57"
    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={api_key}"
    
    # Get the latitude and longitude for the city
    geo_response = requests.get(geocoding_url).json()
    
    if len(geo_response) > 0:
        lat = geo_response[0]['lat']
        lon = geo_response[0]['lon']
        
        # Call the One Call API 3.0 with the lat/lon coordinates
        weather_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=metric&appid={api_key}"
        weather_response = requests.get(weather_url).json()
        return weather_response
    else:
        return {"cod": "404", "message": "City not found"}

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    weather_data = get_weather(city)
    
    # Debug: print the raw response from the API
    print(weather_data)

    # Check if the API response contains the expected keys
    if weather_data and "current" in weather_data:
        try:
            current = weather_data["current"]
            weather = current["weather"][0]
            wind = current["wind_speed"]

            # Weather details to pass to the frontend
            data = {
                "city": city,
                "temperature": current["temp"],
                "feels_like": current["feels_like"],
                "humidity": current["humidity"],
                "description": weather["description"],
                "wind_speed": wind
            }
            return render_template('index.html', weather_data=data)
        except KeyError:
            error = "Unexpected data structure in API response."
            return render_template('index.html', error=error)
    else:
        error = f"City {city} not found."
        return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
