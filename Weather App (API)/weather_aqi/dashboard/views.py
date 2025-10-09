import requests
from django.shortcuts import render

# Complete list of Tamil Nadu cities
TN_CITIES = [
    "Ariyalur","Chengalpattu","Chennai","Coimbatore","Cuddalore","Dharmapuri",
    "Dindigul","Erode","Kanchipuram","Kanyakumari","Karur","Krishnagiri",
    "Madurai","Nagapattinam","Namakkal","Nilgiris","Perambalur","Pudukkottai",
    "Ramanathapuram","Salem","Sivaganga","Tenkasi","Thanjavur","Theni",
    "Thoothukudi","Tiruchirappalli","Tirunelveli","Tirupattur","Tiruppur",
    "Tiruvallur","Tiruvarur","Vellore","Viluppuram","Virudhunagar"
]

def home(request):
    weather_data = None
    aqi_data = None
    city = request.GET.get('city')

    if city:
        api_key = "28c2c70d9005efb576f076b3c0fbfcd2"  # 🔑 replace with your OpenWeatherMap API key

        # Fetch Weather Data
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        weather_response = requests.get(weather_url).json()

        if weather_response.get('cod') == 200:
            weather_data = {
                'city': city.title(),
                'temperature': weather_response['main']['temp'],
                'humidity': weather_response['main']['humidity'],
                'wind': weather_response['wind']['speed'],
                'description': weather_response['weather'][0]['description'].title(),
                'icon': weather_response['weather'][0]['icon'],  # weather icon
            }

            # Fetch AQI Data
            lat = weather_response['coord']['lat']
            lon = weather_response['coord']['lon']
            aqi_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
            aqi_response = requests.get(aqi_url).json()

            aqi_index = aqi_response['list'][0]['main']['aqi']

            aqi_level = {
                1: 'Good 🌿',
                2: 'Fair 🌤️',
                3: 'Moderate 🌫️',
                4: 'Poor 😷',
                5: 'Very Poor ☠️'
            }

            aqi_data = {
                'aqi': aqi_index,
                'quality': aqi_level.get(aqi_index, 'Unknown'),
                'pm2_5': aqi_response['list'][0]['components']['pm2_5'],
                'pm10': aqi_response['list'][0]['components']['pm10'],
                'no2': aqi_response['list'][0]['components']['no2'],
                'so2': aqi_response['list'][0]['components']['so2'],
                'co': aqi_response['list'][0]['components']['co'],
            }

    return render(request, 'dashboard/home.html', {
        'weather': weather_data,
        'aqi': aqi_data,
        'cities': TN_CITIES
    })
