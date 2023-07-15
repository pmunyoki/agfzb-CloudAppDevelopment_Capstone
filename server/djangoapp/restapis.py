import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview


def get_request(url, api_key=None, **kwargs ):
    print("GET from {} ".format(url))
    if api_key:
        try:
            params = dict()
            params["text"] = kwargs["text"]
            params["language"] ="en"
            params["features"] = {"sentiment": { "Targets": ["good","satisfactory", "amazing","great"]}}
            params["keywords"] = {"emotion": True}
            response = requests.post(url, headers={'Content-Type': 'application/json'}, json=params,  auth=HTTPBasicAuth('apikey', api_key) )
            print(response.status_code)
        except:
            print("Network exception occurred")
    else:
        try:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        except:
            print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result
    
        for row in dealers:
            dealer = row['doc']
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                    id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                    short_name=dealer["short_name"],
                                    st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results

def post_request(url, json_payload, **kwargs):
    
    try:
        response = requests.post(url, json=json_payload, params=kwargs)
        print("With status {} ".format(response.status_code))
        json_data = json.loads(response.text)
    except:
        print("Network exception occurred")
        return
    return json_data


def get_dealer_reviews_from_cf(url):
    reviews = []
    if reviews_data:=get_request(url):
        for review in reviews_data:
            sentiment = analyze_review_sentiments(review['review'])
            sent_value = sentiment['sentiment']['document']['label']
            reviews_obj = DealerReview(id=review.get('id',"none"), name=review.get('name','none') , dealership=review.get('dealership','none'), \
                                       review=review.get('review', 'none'), purchase=review.get('purchase','none'), purchase_date=review.get('purchase_date', 'none'),\
                                        car_make=review.get('car_make','none'), car_model=review.get('car_model','none'), car_year=review.get('car_year','none'),\
                                        sentiment=sent_value)
            
            reviews.append(reviews_obj)
    return reviews

def analyze_review_sentiments(review):
    text = {"text": review}
    api_key ="21K55zehKYLrpR7Kf4NJcNa9b4Q8fZ-sUK0vunhs8KnI"
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/31ec9a52-c2f7-48d2-b0e7-cd1237ce8783/v1/analyze?version=2019-07-12"
    sentiment = get_request(url, api_key, **text)
  
    return sentiment



