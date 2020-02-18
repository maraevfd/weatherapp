import requests
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import City
from .forms import CityForm


def index(request):
    appid = 'fa17f08ec9b8437e52f394c9a1e87fb6'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'id': city.id,
            'city': city.name,
            'temp': res['main']['temp'],
            'icon': res['weather'][0]['icon'],
            'feels_like': res['main']['feels_like'],
        }

        all_cities.append(city_info)

    context = {'all_info': all_cities, 'form': form}

    return render(request, 'weather/index.html', context)


def delete(request, id):
    city = City.objects.get(id=id)
    city.delete()

    return HttpResponseRedirect('/')

