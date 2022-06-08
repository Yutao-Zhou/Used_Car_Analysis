import json
import requests
def get_carmax_page_api():
    """Get data for a page of 20 vehicles from the CarMax API."""
    # make a GET request to the vehicles endpoint
    page_url = 'https://api.carmax.com/v1/api/vehicles?apikey=adfb3ba2-b212-411e-89e1-35adab91b600'
    response = requests.get(page_url)
    
    # get JSON from requests and return the results subsection
    return response.json()['Results']
print(get_carmax_page_api())
