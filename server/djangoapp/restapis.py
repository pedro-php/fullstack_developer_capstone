# Uncomment the imports below before you add the function code
import os

import requests
from dotenv import load_dotenv


load_dotenv()

backend_url = os.getenv(
    "backend_url",
    default="http://localhost:3030",
)

sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url",
    default="http://localhost:5000/",
)


def get_request(endpoint, **kwargs):
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
        print(
            f"[DEBUG] Response text (first 500 chars): "
            f"{response.text[:500]}"
        )

        try:
            data = response.json()
            print(f"[DEBUG] JSON parsed successfully: {data}")
            return data
        except ValueError:
            print("[ERROR] Response is not valid JSON")
            return None

    except requests.exceptions.RequestException as exc:
        print(f"[ERROR] Network exception occurred: {exc}")
        return None


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text

    try:
        response = requests.get(request_url, timeout=10)
        return response.json()

    except requests.exceptions.RequestException as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


def post_review(data_dict):
    request_url = backend_url + "/insert_review"

    try:
        response = requests.post(request_url, json=data_dict, timeout=10)
        print(response.json())
        return response.json()

    except requests.exceptions.RequestException:
        print("Network exception occurred")
        