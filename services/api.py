import requests

def fetch_data():
    res = requests.get("https://www.apicountries.com/countries")
    res.raise_for_status()
    return res.json()
