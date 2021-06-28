# Flask import
from flask import Flask, request, render_template
import requests
from requests import api

app = Flask(__name__)

api_key = "e701ceff202ee46372e810ef7d611d0b"
url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=e701ceff202ee46372e810ef7d611d0b"

@app.get('/')
def index():
    return "<h1>Welcome to the Weather App</h1>"

def kelvin_to_celsius(temp):
    to_kelvin = temp - 273.15

    return round(to_kelvin)

@app.post('/weather')
def postWeatherDetails():
    city = request.form['city']
    
    result = requests.get(url.format(city)).json()
    weather = {}
    min_temp = kelvin_to_celsius(result['main']['temp_min'])
    max_temp = kelvin_to_celsius(result['main']['temp_max'])
    parameter = {
        'min_temp' : min_temp,
        'max_temp' : max_temp,
        'pressure' : result['main']['pressure'],
        'humidity' : result['main']['humidity'],
        'wind' : result['wind']['speed'],
        'sunrise' : result['sys']['sunrise'], 
        'sunset' : result['sys']['sunset'] 
    }
    weather['city'] = result['name']
    description = result['weather'][0]['description']
    weather['description'] = description.title()
    weather['icon'] = result['weather'][0]['icon']
    weather['parameters'] = parameter
    weather['temperature'] = kelvin_to_celsius(result['main']['temp'])

    print(weather, len(weather))
    weather_ = []
    weather_.append(weather)

    return render_template('index.html', weather_data=weather_)


@app.get('/weather')
def getWeatherPage():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
