# views.py
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import City
import requests

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')  
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def home(request):
    return render(request, 'weather/home.html')

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def weather(request):
    if request.method == 'POST':
        city_name = request.POST['city']
        api_key = '6a4bfe57a3c12c801b83bd3c13d22907'
        api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'

        response = requests.get(api_url)
        data = response.json()

        if response.status_code == 200:
            temperature_kelvin = data['main']['temp']
            temperature_celsius = kelvin_to_celsius(temperature_kelvin)
            city = City(name=city_name)
            city.save()
            return render(request, 'weather/weather.html', {'city': city, 'temperature': temperature_celsius})
        else:
            error_message = 'City not found'
            return render(request, 'weather/weather.html', {'error_message': error_message})
    else:
        return render(request, 'weather/weather.html')
