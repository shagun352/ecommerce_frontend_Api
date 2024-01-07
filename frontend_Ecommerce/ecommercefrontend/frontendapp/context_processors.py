from django.shortcuts import render
from django.views import View
from django.contrib import messages
import requests  

API_URL = "http://127.0.0.1:8000"
def all_categories(request):
    try:
        api_url = f"{API_URL}/product/get-all-categories"
        api_response = requests.get(api_url)
        if api_response.status_code == 200:
            category_data = api_response.json()
            return {'all_categories': category_data}
    except Exception as e:
        pass  
    return {}  