from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace with your OpenWeatherMap API key
API_KEY = "YOUR_API_KEY"

# Function to get weather data
def get_weather(city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city_name + "&appid=" + API_KEY + "&units=metric"
    response = requests.get(complete_url)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    weather_data = get_weather(city)
    
    if weather_data["cod"] != "404":
        main = weather_data["main"]
        weather = weather_data["weather"][0]
        wind = weather_data["wind"]

        # Weather details to pass to the frontend
        data = {
            "city": city,
            "temperature": main["temp"],
            "feels_like": main["feels_like"],
            "humidity": main["humidity"],
            "description": weather["description"],
            "wind_speed": wind["speed"]
        }
        return render_template('index.html', weather_data=data)
    else:
        error = f"City {city} not found."
        return render_template('index.html', error=error)

if __name__ == "__main__":
    app.run(debug=True)
