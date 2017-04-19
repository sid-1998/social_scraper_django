from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from models import *
from django.contrib.auth.decorators import login_required

from bs4 import BeautifulSoup
import requests
import re
import time
import urllib2

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required(login_url='/signup')
def index(request):
    current_user = request.user
    try:
        Coder = Codechef.objects.get(user = current_user)
        cUsername = Coder.username
        cUame = Coder.name
        cRating = Coder.rating
        cGlobal = Coder.globalRank
        cCountry = Coder.countryRank
        cPlace = Coder.country

    except:
        cUsername = cUame = cRating = cGlobal = cCountry = cPlace = None
    try:
        quora = Quora.objects.get(user = current_user).username
    except:
        quora = None

    context = {
        'user' : current_user,
        'cUsername' : cUsername,
        'cRating' : cRating,
        'cGlobal' : cGlobal,
        'cCountry' : cCountry,
        'cPlace' : cPlace,
        'quora': quora,
    }

    return render(request, 'home.html', context)

def codechef(request):
    if request.method == 'POST':
        username =  request.POST.get('username')
        user =  request.user

        url = 'https://www.codechef.com/users/' + username
        response = urllib2.urlopen(url)
        soup = BeautifulSoup(response,'html.parser')

        name = soup.select_one('body > main > div > div > div > div > div > header > h2').text
        rating = soup.find('div', {"class":'rating-number'}).text
        globalRank = soup.find_all('ul', {"class":'inline-list'})[1].find_all('strong')[0].text
        countryRank = soup.find_all('ul', {"class":'inline-list'})[1].find_all('strong')[1].text
        country = soup.find('span', {'class':'user-country-name'}).text


        code = Codechef(
            username=username,
            user=user,
            name=name,
            rating=rating,
            globalRank=globalRank,
            countryRank=countryRank,
            country = country,
            )

        code.save()

    return redirect('/')

def quora(request):
    if request.method == 'POST':
        username =  request.POST.get('username')
        user =  request.user
        quora = Quora(username=username, user=user)
        quora.save()

    return redirect('/')
