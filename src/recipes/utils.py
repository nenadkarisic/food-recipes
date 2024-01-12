import os
import requests


def verify_email(email):
    url = "https://api.hunter.io/v2/email-verifier"
    params = {
        "email": email,
        "api_key": os.environ.get('HUNTER_API_KEY')
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
    return response.json()
