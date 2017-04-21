from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import IntegerField, Max, Min
from django.db.models.functions import Cast
from django.contrib.auth.models import User

from bs4 import BeautifulSoup
import requests
# import re
# import time
import urllib2
import operator

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
    return render(request, 'signup.html', context={'form': form})

@login_required(login_url='/signup')
def index(request):
    current_user = request.user
    try:
        Coder = Codechef.objects.get(user = current_user)
        cUsername = Coder.username
        cName = Coder.name
        cRating = Coder.rating
        cGlobal = Coder.globalRank
        cCountry = Coder.countryRank
        cPlace = Coder.country

    except:
        cUsername = cUame = cRating = cGlobal = cCountry = cPlace = cName = None
    try:
        quora = Quora.objects.get(user = current_user)
        qUsername = quora.username
        qAnswers = quora.answers
        qTCount = quora.totalViews
        qMCount = quora.monthViews
        qName = quora.name

    except:
        qUsername = qAnswers = qTCount = qMCount = qName = None

    context = {
        'user' : current_user,
        'cUsername' : cUsername,
        'cName' : cName,
        'cRating' : cRating,
        'cGlobal' : cGlobal,
        'cCountry' : cCountry,
        'cPlace' : cPlace,
        'qUsername' : qUsername,
        'qAnswers' : qAnswers,
        'qTCount' : qTCount,
        'qMCount' : qMCount,
        'qName' : qName,
    }

    return render(request, 'home.html', context=context)

def codechef(request):
    if request.method == 'POST':
        username =  request.POST.get('username')
        user =  request.user

        url = 'https://www.codechef.com/users/' + username
        response = urllib2.urlopen(url)
        soup = BeautifulSoup(response,'html.parser')

        try:
            name = soup.select_one('body > main > div > div > div > div > div > header > h2').text
        except:
            name = 'Not Found'
        try:
            rating = soup.find('div', {"class":'rating-number'}).text
        except:
            rating = 'Not Found'
        try:
            globalRank = soup.find_all('ul', {"class":'inline-list'})[1].find_all('strong')[0].text
        except:
            globalRank = 'Not Found'
        try:
            countryRank = soup.find_all('ul', {"class":'inline-list'})[1].find_all('strong')[1].text
        except:
            countryRank = 'Not Found'
        try:
            country = soup.find('span', {'class':'user-country-name'}).text
        except:
            country = 'Not Found'

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

def delCodechef(request):
    if request.method == 'POST':
        Codechef.objects.filter(user=request.user).delete()

    return redirect('/')

def delQuora(request):
    if request.method == 'POST':
        Quora.objects.filter(user=request.user).delete()

    return redirect('/')

def quora(request):
    if request.method == 'POST':
        username =  request.POST.get('username')

        url = 'https://www.quora.com/profile/' + username
        response = urllib2.urlopen(url)
        soup = BeautifulSoup(response, 'html.parser')
        try:
            answers = soup.find('div', {'class':'list_header'}).text.split()[0]
            if answers == 'Answers':
                answers = 'Not Found'
        except:
            answers = 'Not Found'
        try:
            totalViews = soup.find('div', {'class':'AboutListItem AnswerViewsAboutListItem'}).find('span',{'class':'main_text'}).text.split()[0]
        except:
            totalViews = 'Not Found'
        try:
            monthViews = soup.find('div', {'class':'AboutListItem AnswerViewsAboutListItem'}).find('span',{'class':'detail_text'}).text.split()[0]
        except:
            monthViews = 'Not Found'
        try:
            name = soup.find('div', {'class':'ProfileNameAndSig'}).find('span', {'class':'user'}).text
        except:
            name = 'Not Found'

        user =  request.user
        quora = Quora(
            username=username,
            user=user,
            name=name,
            totalViews=totalViews,
            monthViews=monthViews,
            answers=answers,
        )
        quora.save()

    return redirect('/')

@login_required(login_url='/signup')
def stats(request):
    if not request.user.is_superuser:
        return redirect('/')
    else:
        coders = Codechef.objects.annotate(ratings=Cast('rating',IntegerField())).order_by('-ratings')
        quoras = Quora.objects.annotate(answer=Cast('answers',IntegerField())).order_by('-answer')
        users = User.objects.all()

        maxCodechef = coders.aggregate(Max('ratings'))['ratings__max']
        maxCodechef = float(maxCodechef)
        minCodechef = coders.aggregate(Min('ratings'))['ratings__min']
        minCodechef = float(minCodechef)

        maxQuora = quoras.aggregate(Max('answer'))['answer__max']
        maxQuora = float(maxQuora)
        minQuora = quoras.aggregate(Min('answer'))['answer__min']
        minQuora = float(minQuora)

        # calculating score for users
        for user in users:
            codechefScore = list(coders.filter(user=user))[0].rating
            codechefScore = float(codechefScore)
            codechefScore = (codechefScore - minCodechef)/(maxCodechef - minCodechef)
            user.codechefScore = codechefScore

            quoraScore = list(quoras.filter(user=user))[0].answers
            quoraScore = float(quoraScore)
            quoraScore = (quoraScore - minQuora)/(maxQuora - minQuora)
            user.quoraScore = quoraScore

            user.totalScore = (codechefScore * 1.0 + quoraScore * 1.0) / 2.0

        users = list(users)

        # sorting list
        users.sort(key = operator.attrgetter('totalScore'), reverse=True)

        context = {
            'coders': coders,
            'quoras': quoras,
            'users': users
        }
        return render(request, 'stats.html', context=context)
