from django.shortcuts import render,redirect
from django.views import View
import requests
from django.contrib import messages
import time

API_URL = "http://127.0.0.1:8000"

def index(request): 
    return render(request, "product/index.html") 
    
class RegisterView(View):
    template_name = "product/register.html"
    url = f"{API_URL}/users/register"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        country = request.POST.get('country')

        data = {
            'first_name': first_name,
            'last_name': last_name,
            'password': password,
            'password2': password2,
            'email': email,
            'gender': gender,
            'city': city,
            'country': country,
        }
        
        response = requests.post(self.url, json=data)

        if response.status_code == 201:  
            messages.success(request, "User registered successfully.")
        elif response.status_code == 400:  # Bad Request (validation error)
            error_messages = response.json().get('error_messages', {})
            for field, errors in error_messages.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return render(request, self.template_name, data)
        else:
            messages.error(request, "Something went wrong. Please try again.")

        return render(request, self.template_name)
    
class LoginView(View):
    template_name = "product/signin.html"
    url = f"{API_URL}/users/login"

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get('password')
        data = {
            "email": email,
            "password": password,
        }
        response = requests.post(self.url, json=data)
        response_data = response.json()
        print(response_data)
        
        if response.status_code == 200:
            request.session['access_token'] = response_data.get('access')
            request.session['user_info'] = response_data.get('user_info')
            user_info = request.session.get('user_info')
            print(user_info,"hii")
            messages.success(request, "User logged in successfully.")  
        else:
            error_message = response_data.get('message')
            messages.error(request, error_message)    
        return render(request, self.template_name)
    

class LogoutView(View):
    def get(self, request):
        print("----------------")
        try:
            print("tryyy11y")
            refresh_token = request.session.get('access_token')
            print(refresh_token)
            api_logout_url = f"{API_URL}/users/logout/"
            api_response = requests.post(api_logout_url, json={"refresh": refresh_token})
            if api_response.status_code == 200:
                del request.session['access_token']
                messages.success(request,"logout sucessfully")
                
            else:
                messages.error(request, "error")
        except Exception as e:
            messages.error(request,e)
        return render(request,'product/index.html')  
        

class ProductView(View):
    template_name = 'product/store.html'

    def get(self, request, category_slug=None):
        try:
            if category_slug is not None:
                api_url = f"{API_URL}/product/categories/{category_slug}/"
            else:
                api_url = f"{API_URL}/product/product/"

            api_response = requests.get(api_url)

            if api_response.status_code == 200:
                product_data = api_response.json()
                print(product_data, "dataaaaaaaaaa")

                context = {'list_product': product_data,
                           'total_length': len(product_data)
                           }

                return render(request, self.template_name, context)
            else:
                messages.error(request, f"Failed to fetch products. Status code: {api_response.status_code}")
        except Exception as e:
            messages.error(request, f"Error: {e}")

        return render(request, self.template_name)

class AllCategories(View):
    template_name = 'product/store.html'
    def get(self,request):
        try:
            api_url = f"{API_URL}/product/get-all-categories"
            api_response = requests.get(api_url)
            if api_response.status_code == 200:
                category_data = api_response.json()
                print(category_data)
                context = {
                    'all_categories':category_data
                }
                print(context)
                return render(request, self.template_name,context)
            else:
                messages.error(request, f" Status code: {api_response.status_code}")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return render(request, self.template_name)

class ProductDetail(View):
    template_name = 'product/product-detail.html'

    def get(self,request,pk=None):
        print("getttttttttttttttt")
        try:
            api_url = f"{API_URL}/product/product/{pk}/"
            print("urlllllll===",api_url)
            api_response = requests.get(api_url)
            print(api_response.json())
            if api_response.status_code == 200:
                print(api_response.status_code)
                product_data = api_response.json()
                context = {'product_data':product_data}
                print("context",context)
                return render(request, self.template_name,context)
            else:
                messages.error(request, f" Status code: {api_response.status_code}")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return render(request, self.template_name)
    
class DisplayProductHomePage(View):
    template_name = 'product/index.html'

    def get(self,request):
        try:
            api_url = f"{API_URL}/product/product/"
            print("urlllllll===",api_url)
            api_response = requests.get(api_url)
            print(api_response.json())
            if api_response.status_code == 200:
                print(api_response.status_code)
                product_data = api_response.json()
                context = {'product_data':product_data}
                print("context",context)
                return render(request, self.template_name,context)
               
            else:
                messages.error(request, f" Status code: {api_response.status_code}")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return render(request, self.template_name)

