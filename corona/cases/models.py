from django.db import models
import requests

api = 'https://pomber.github.io/covid19/timeseries.json'
requested_url = requests.get(api)
json_list = requested_url.json()
countries = list(json_list.keys())

COUNTRIES=[]

for i in range(len(countries)):
    tupple = (countries[i], countries[i])
    COUNTRIES.append(tupple)

COUNTRIES = tuple(COUNTRIES)

# Create your models here.
class url_request(models.Model):
    country = models.CharField(choices=COUNTRIES,max_length=1000)