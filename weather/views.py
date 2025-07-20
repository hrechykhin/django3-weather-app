import requests
from django.shortcuts import render, redirect
from weather.models import City
from weather.forms import CityForm
from django.conf import settings


def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + settings.OPENWEATHERMAP_KEY

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CityForm()

    cities = City.objects.all()
    all_cities = []

    for city in cities:
        try:
            res = requests.get(url.format(city.name)).json()
            if res.get("cod") != 200:
                continue

            city_info = {
                'city': res["name"],
                'temp': res["main"]["temp"],
                'icon': res["weather"][0]["icon"]
            }
            all_cities.append(city_info)

        except Exception as e:
            continue

    context = {
        'all_info': all_cities,
        'form': form
    }

    return render(request, 'weather/index.html', context)


def deletecity(request):
    cities = City.objects.all()
    if request.method == 'POST':
        cities.delete()
        return redirect('home')
