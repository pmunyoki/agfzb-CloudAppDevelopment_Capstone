from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

dealerships = []
# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')
# ...


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
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

# ...

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')
# ...

# Create a `registration_request` view to handle sign up request
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
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/0e19a713-5cb0-469a-9d5d-33bd21ae8720/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        context['dealerships']=dealerships

        return render(request, 'djangoapp/index.html', context)
    


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == 'GET':
        context = {}
        url = f"https://us-south.functions.appdomain.cloud/api/v1/web/0e19a713-5cb0-469a-9d5d-33bd21ae8720/review/review/?dealership={dealer_id}"
        reviews = get_dealer_reviews_from_cf(url)
        print(reviews)
        context['reviews']= reviews
        for dealer in dealerships:
            if dealer['id'] == dealer_id:
                context['dealer']= dealer["full_name"]
        return render(request, 'djangoapp/dealer_details.html', context)
   
# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.user.is_authenticated:
        review = dict()
        review['name'] = "Upkar Lidder"
        review['dealership'] = dealer_id
        review['review'] = "Poor service"
        review['purchase'] = "False"
        review['purchase_date'] = "02/16/2021"
        review['car_make'] = "Audi"
        review['car_model'] = "car"
        review['car_year'] = "2016"
        data = dict()
        data['review'] = review
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/0e19a713-5cb0-469a-9d5d-33bd21ae8720/review/post"
        response = post_request(url, data)
        if response:
            print("Your review was submitted successfully")
        else:
            print("not successful")
        
    return HttpResponse(response)
        
        

        #else:
            #print("Please log in to post a review")


...

