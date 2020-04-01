from django.shortcuts import render, HttpResponse,redirect
import requests
import json
from bs4 import BeautifulSoup
from .forms import search_form

# Create your views here.
api = 'https://pomber.github.io/covid19/timeseries.json'
bing = requests.get('https://www.bing.com/covid')
requested_url = requests.get(api)
json_list = requested_url.json()
countries = list(json_list.keys())


def index(request):
    world = len(countries)
    cases =[]
    for i in range(world):
        cases.append(json_list[countries[i]])
    total_days = len(cases[0])
    date = []
    confirmed = []
    deaths = []
    recovered = []
    for i in range(total_days):
        cnf = 0
        dth = 0
        rec = 0
        date.append(cases[0][i]['date'])
        for x in range(world):
            cnf=cnf+int(cases[x][i]['confirmed'])
            dth=dth+int(cases[x][i]['deaths'])
            rec=rec+int(cases[x][i]['recovered'])
        confirmed.append(cnf)
        deaths.append(dth)
        recovered.append(rec)
    if request.method=="POST":
        form = search_form(request.POST)
        if form.is_valid():
            print('valid')
            cntry = form.cleaned_data['country']
            url = '/region/'
            url = url + str(cntry)
            return redirect(url)

        else:
            form = search_form(request.POST)
    else:
        form = search_form()

    context = {'date':date,'confirmed':confirmed,'recovered':recovered,'deceased':deaths,'form':form}
    return render(request, 'index.html',context)


def region(request, t):
    requested_country = str(t)
    cases = json_list[requested_country]
    total_days = len(cases)
    date = []
    confirmed = []
    deaths = []
    recovered = []
    for i in range(total_days):
        date.append(cases[i]['date'])
        confirmed.append(cases[i]['confirmed'])
        deaths.append(cases[i]['deaths'])
        recovered.append(cases[i]['recovered'])
    context = {'date': date, 'confirmed': confirmed, 'recovered': recovered, 'deceased': deaths,'country':requested_country}
    return render(request, 'region.html',context)
