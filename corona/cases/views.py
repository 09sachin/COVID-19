from django.shortcuts import render, HttpResponse
import requests
import json
from bs4 import BeautifulSoup

# Create your views here.
api = 'https://bing.com/covid/graphdata'
bing = requests.get('https://www.bing.com/covid')


def index(request):
    r = requests.get(api)
    x = r.json()
    print(x)
    t = []
    change = []
    date = []
    recover = []
    fatal = []
    active = []
    percent_active = []
    closed = []
    percent_closed = []
    soup2 = BeautifulSoup(bing.content, features="html.parser")
    text = soup2.get_text(strip=True)
    m = text.split()
    n = len(m)
    tokens = m[n - 1]
    token = tokens

    tc = token.split('world')
    gggg = len(tc)
    tkn = tc[gggg - 1]
    tkn = tkn[5:]

    characters_to_remove = '"'
    characters_to_replace = ','

    for character in characters_to_remove:
        tkn = tkn.replace(character, "")

    for character in characters_to_replace:
        tkn = tkn.replace(character, ". ")

    first = ";"
    second = "}"

    for character in first:
        tkn = tkn.replace(character, "")
    for character in second:
        tkn = tkn.replace(character, "")

    live = tkn
    splt = live.split('.')
    confirmed = splt[0]
    death = splt[1]
    recovered = splt[2]
    updated = splt[3]
    confirmed1 = confirmed.split(':')
    confirmed2 = confirmed1[1]
    death1 = death.split(':')
    death2 = death1[1]
    recovered1 = recovered.split(':')
    recovered2 = recovered1[1]

    updated2 = updated

    for i in range(len(x['world'])):
        b = x['world'][i]['confirmed']
        t.append(b)
        date.append(x['world'][i]['date'])
        recover.append(x['world'][i]['recovered'])
        fatal.append(x['world'][i]['fatal'])
        a = x['world'][i]['confirmed'] - x['world'][i]['recovered'] - x['world'][i]['fatal']
        active.append(a)
        cl = (x['world'][i]['recovered'] + x['world'][i]['fatal'])
        closed.append(cl)
        pc = "{:.3f}".format(float(float(cl / b) * 100))
        percent_closed.append(pc)

        if i == 0:
            diff = t[i] - 0
            change.append(diff)
            p = "{:.3f}".format(float(float(diff / a) * 100))
            percent_active.append(p)
        else:
            diff = t[i] - t[i - 1]
            change.append(diff)
            p = "{:.3f}".format(float(float(diff / a) * 100))
            percent_active.append(p)

        # print(x['world'][i]['confirmed'], "   ", diff, '\n')

    context = {'change': change, 'confirmed': t, 'date': date, 'recovered': recover, 'deceased': fatal,
               'active': active, 'closed': closed, 'percent_closed': percent_closed,
               'p_active': percent_active, 'conf': confirmed2, 'dead': death2, 'rec': recovered2, 'time': updated2}
    return render(request, 'index.html', context)


def region(request, t):
    try:
        soup2 = BeautifulSoup(bing.content, features="html.parser")
        text = soup2.get_text(strip=True)
        tokens = text.split()
        country = '"' + t + '"'
        cnt = t
        loc = 0
        for x in range(len(tokens)):
            pos = tokens[x].find(country)
            if pos != -1:
                loc = x
        ind = tokens[loc].split(country)
        li = (len(ind))
        india = ind[li - 1].split('"lastUpdated"')
        tkn = india[0]
        tkn = tkn[3:]
        characters_to_remove = '"'
        characters_to_replace = ','

        for character in characters_to_remove:
            tkn = tkn.replace(character, "")

        for character in characters_to_replace:
            tkn = tkn.replace(character, ". ")
        first = ";"
        second = "}"

        for character in first:
            tkn = tkn.replace(character, "")
        for character in second:
            tkn = tkn.replace(character, "")

        live = tkn
        splt = live.split('.')
        confirmed = splt[0]
        death = splt[1]
        recovered = splt[2]
        confirmed1 = confirmed.split(':')
        confirmed2 = confirmed1[1]
        death1 = death.split(':')
        death2 = death1[1]
        recovered1 = recovered.split(':')
        recovered2 = recovered1[1]

        context = {'conf': confirmed2, 'dead': death2, 'rec': recovered2, 'name': cnt}

        return render(request, 'region.html', context)
    except:
        return HttpResponse("<h2 style='test-align:center;padding-top:40px'>Requested region not found</h2>")
