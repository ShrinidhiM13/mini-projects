import requests
from flask import Flask, request, render_template

app = Flask(__name__)

# Function to get weather data using the Current Weather Data API
def get_weather(city):
    api_key = "06dffbeb7c0c4a146315d3323ac03c57"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    
    # Get the weather data
    weather_response = requests.get(weather_url).json()

    # Return the response
    return weather_response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    weather_data = get_weather(city)
    
    # Debug: print the raw response from the API
    print(weather_data)

    # Check if the API response contains the expected keys
    if weather_data and "main" in weather_data:
        try:
            main = weather_data["main"]
            weather = weather_data["weather"][0]
            wind = weather_data["wind"]["speed"]

            # Weather details to pass to the frontend
            data = {
                "city": city,
                "temperature": main["temp"],
                "feels_like": main["feels_like"],
                "humidity": main["humidity"],
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
