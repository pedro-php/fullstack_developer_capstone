# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5000/")

# def get_request(endpoint, **kwargs):
def get_request(endpoint, **kwargs):
    # Build query string manually
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"

    request_url = backend_url + endpoint
    if params:
        request_url += "?" + params.rstrip("&")

    print(f"[DEBUG] GET request to: {request_url}")

    try:
        response = requests.get(request_url, timeout=10)
        print(f"[DEBUG] Status code: {response.status_code}")
        print(f"[DEBUG] Response text (first 500 chars): {response.text[:500]}")

        try:
            data = response.json()
            print(f"[DEBUG] JSON parsed successfully: {data}")
            return data
        except ValueError:
            print("[ERROR] Response is not valid JSON")
            return None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network exception occurred: {e}")
        return None

# def analyze_review_sentiments(text):
def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url+"analyze/"+text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")

# def post_review(data_dict):
def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url,json=data_dict)
        print(response.json())
        return response.json()
    except:
        print("Network exception occurred")
