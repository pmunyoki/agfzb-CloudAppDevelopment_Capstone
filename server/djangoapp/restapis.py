import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=None, **kwargs ):
    print("GET from {} ".format(url))
    if api_key:
        try:
            # Call get method of requests library with URL and parameters
            params = dict()
            params["text"] = kwargs["text"]
            params["language"] ="en"
            #params["version"] =  '2022-04-07'
            params["features"] = {"sentiment": { "Targets": ["good","satisfactory", "amazing","great"]}}
            params["keywords"] = {"emotion": True}
            response = requests.post(url, headers={'Content-Type': 'application/json'}, json=params,  auth=HTTPBasicAuth('apikey', api_key) )
            print(response.status_code)
        except:
            # If any error occurs
            print("Network exception occurred")
    else:
        try:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        except:
            # If any error occurs
            print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    print(json_data)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                    id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                    short_name=dealer["short_name"],
                                    st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)



# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url):
    reviews = []
    if reviews_data:=get_request(url):
        for review in reviews_data:
            reviews_obj = DealerReview(id=review.get('id',"none"), name=review['name'], dealership=review['dealership'], \
                                       review=review['review'], purchase=review['purchase'], purchase_date=review['purchase_date'],\
                                        car_make=review['car_make'], car_model=review['car_model'], car_year=review['car_year'],\
                                        sentiment="")
            sentiment = analyze_review_sentiments(review['review'])
            reviews.append(reviews_obj)
    return reviews

# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(review):
    text = {"text": review}
    api_key ="21K55zehKYLrpR7Kf4NJcNa9b4Q8fZ-sUK0vunhs8KnI"
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/31ec9a52-c2f7-48d2-b0e7-cd1237ce8783/v1/analyze?version=2019-07-12"
    sentiment = get_request(url, api_key, **text)
  
    return sentiment
# - Get the returned sentiment label such as Positive or Negative


