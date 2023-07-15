from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarMake
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, get_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


def about(request):
    return render(request, 'djangoapp/about.html')

def car_models(dealer_id):
    models = CarModel.objects.filter(dealer_id=dealer_id).all()
    print(models)
    return models

def get_carmake(id):
    carmake = get_object_or_404(CarMake, pk=id)
    print(carmake)
    return carmake

def contact(request):
    return render(request, 'djangoapp/contact.html')

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['login_message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html')


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/0e19a713-5cb0-469a-9d5d-33bd21ae8720/dealership-package/get-dealership"
        dealerships = get_dealers_from_cf(url)
        context['dealerships']=dealerships

        return render(request, 'djangoapp/index.html', context)
    

def get_dealer_by_id(dealer_id):
    url = f"https://us-south.functions.appdomain.cloud/api/v1/web/0e19a713-5cb0-469a-9d5d-33bd21ae8720/dealership-package/get_dealership_by_id?id={dealer_id}"
    dealer = get_request(url)
    return dealer

def get_dealer_details(request, dealer_id):
    if request.method == 'GET':
        context = {}
        url = f"https://us-south.functions.appdomain.cloud/api/v1/web/0e19a713-5cb0-469a-9d5d-33bd21ae8720/review/review/?dealership={dealer_id}"
        reviews = get_dealer_reviews_from_cf(url)
        dealership = get_dealer_by_id(dealer_id)[0]
        context['reviews']= reviews
        context['dealer']= dealership

       
        return render(request, 'djangoapp/dealer_details.html', context)
   
def add_review(request, dealer_id):
    context = {}
    if request.user.is_authenticated:
        if request.method == 'GET':
            url = "https://us-south.functions.appdomain.cloud/api/v1/web/0e19a713-5cb0-469a-9d5d-33bd21ae8720/review/post"
            models = car_models(dealer_id)
            dealership = get_dealer_by_id(dealer_id)[0]
            context['dealer'] = dealership["full_name"]
            context['dealer_id'] = dealer_id
            context['models'] = models

        if request.method == 'POST': 
            if request.POST.get('purchasecheck', False):
                purchase = True
            else:
                purchase  = False
            review = dict()
            review['name'] = "Upkar Lidder"
            review['dealership'] = dealer_id
            review['review'] = request.POST['content']
            review['purchase'] = purchase
            if purchase == True:
                car_model_id= request.POST['car']
                car = get_object_or_404(CarModel, pk=car_model_id)
                review['purchase_date'] = request.POST['purchasedate']
                review['car_make'] = car.car_make.name
                review['car_model'] = car.name
                review['car_year'] = car.year.strftime("%Y") 
            data = dict()
            data['review'] = review
            url = "https://us-south.functions.appdomain.cloud/api/v1/web/0e19a713-5cb0-469a-9d5d-33bd21ae8720/review/post"
            context['dealer_id'] = dealer_id

            response = post_request(url, data)
            if response:
                context['message'] = "Your review has been submitted successfully "
            else:
                context['error'] = "An error occured during submision. Please try again later!"
             
    return render(request, 'djangoapp/add_review.html', context)
    