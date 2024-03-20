from django.shortcuts import render
from django.contrib import messages
import requests
import datetime
import calendar

# Create your views here.
def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'colombo'
    
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={'api'}'
    PARAMS = {'units': 'metric'}

    API_KEY = ''
    SEARCH_ENGINE_ID = ''

    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    data = requests.get(city_url).json()
    count = 1
    search_items = data.get('items')
    image_url = search_items[1]['link']

    try:
        data = requests.get(url, params=PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        windspeed = data['wind']['speed']
        pressure = data['main']['pressure']
        day = datetime.date.today()
        weekday = day.weekday()
        today = calendar.day_name[weekday]

        context = {'description':description , 'icon':icon ,'temp':temp , 'humidity':humidity, 'pressure':pressure, 'windspeed':windspeed, 'day':day, 'weekday':weekday, 'today':today, 'city':city, 'exception_occurred':False, 'image_url':image_url}
        return render(request, 'index.html', context)
    except:
        exception_occurred = True
        messages.error(request,'Entered data is not available to API')

        day = datetime.date.today()
        weekday = day.weekday()
        today = calendar.day_name[weekday]

        context = {'description':'clear sky' , 'icon':icon ,'temp':25 , 'day':day, 'weekday':weekday, 'today':today, 'city':'indore', 'exception_occurred':exception_occurred}
        return render(request, 'index.html', context)