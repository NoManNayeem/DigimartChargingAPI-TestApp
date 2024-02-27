from django.shortcuts import render
from django.views import View

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')



from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

from .models import ChargingSDKs, API_Response

@method_decorator(csrf_exempt, name='dispatch')
class AppView(View):
    def get(self, request, app_name):
        app = get_object_or_404(ChargingSDKs, APP_Name=app_name)
        context = {'app_name': app.APP_Name}
        return render(request, 'welcome.html', context)

    def post(self, request, app_name):
        app = get_object_or_404(ChargingSDKs, APP_Name=app_name)
        if request.META.get('CONTENT_TYPE') == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST.dict()
        charging_api_response = json.dumps(data)
        API_Response.objects.create(
            ChargingAPI_Response=charging_api_response,
            StatusAPI_Response='',
            UnsubscribeAPI_Response='',
        )
        return JsonResponse({"message": "Response stored successfully"})



from django.views import View
from django.shortcuts import render, get_object_or_404
import hashlib
import datetime
import random

from .models import Subscriber, ChargingSDKs


class SubscribeView(View):
    def get(self, request, app_name, phone):
        # Find the subscriber and app
        subscriber = get_object_or_404(Subscriber, Contact=phone)
        app = get_object_or_404(ChargingSDKs, APP_Name=app_name)

        # Given values
        api_secret = app.API_Secret
        api_key = app.API_Key
        redirect_url = app.redirect_url
        print("APP's Redirect URL", redirect_url)

        # Generating current UTC time and a random request ID
        current_time_utc = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        
        # Corrected to concatenate '88' with subscriber's contact for the request_id
        request_id = '88' + subscriber.Contact

        # Creating the signature
        signature_data = f'{api_key}|{current_time_utc}|{api_secret}'
        hashed_signature = hashlib.sha512(signature_data.encode()).hexdigest()

        # Constructing the API endpoint
        api_endpoint = f"https://user.digimart.store/sdk/subscription/authorize?apiKey={api_key}&requestId={request_id}&requestTime={current_time_utc}&signature={hashed_signature}&redirectUrl={redirect_url}"
        print("api_endpoint==",api_endpoint)
        # Rendering the subscription page with the context
        context = {
            'subscriber_name': subscriber.Subscriber_Name,
            'app_name': app.APP_Name,
            'api_endpoint': api_endpoint,
        }
        return render(request, 'subscribe.html', context)
    
    
    

    
    
    

    
    
    
    
#-----Status and UnSubscribe------------#



from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from .models import ChargingSDKs, Subscriber, API_Response
import json
import requests

def send_api_request(url, headers, data):
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return str(e)

class StatusAPIView(View):
    def post(self, request, app_name, phone):
        subscriber = get_object_or_404(Subscriber, Contact=phone)
        app = get_object_or_404(ChargingSDKs, APP_Name=app_name)

        public_ip = app.public_ip
        applicationId = app.APP_ID
        password = app.API_Password
        masked_msisdn = subscriber.masked_msisdn
        request_id = f"88{subscriber.Contact}"

        headers = {
            'Content-Type': 'application/json',
            'X-Forwarded-For': public_ip,
        }

        data = {
            "applicationId": applicationId,
            "password": password,
            "subscriberId": f"tel:{masked_msisdn}"
        }
        
        url = 'https://api.digimart.store/subscription/subscriberChargingInfo'
        request_data_str = send_api_request(url, headers, data)

        try:
            api_response = API_Response.objects.get(request_id=request_id)
            api_response.StatusAPI_Response = request_data_str
            api_response.save()
        except API_Response.DoesNotExist:
            return HttpResponseBadRequest("API Response not found for given request_id")

        return JsonResponse({"message": "Status API response updated successfully"})

class UnsubscribeAPIView(View):
    def post(self, request, app_name, phone):
        subscriber = get_object_or_404(Subscriber, Contact=phone)
        app = get_object_or_404(ChargingSDKs, APP_Name=app_name)

        public_ip = app.public_ip
        applicationId = app.APP_ID
        password = app.API_Password
        masked_msisdn = subscriber.masked_msisdn
        request_id = f"88{subscriber.Contact}"

        headers = {
            'Content-Type': 'application/json',
            'X-Forwarded-For': public_ip,
        }

        data = {
            "applicationId": applicationId,
            "password": password,
            "subscriberId": f"tel:{masked_msisdn}",
            "action": "0"
        }
        
        url = 'https://api.digimart.store/subs/unregistration'
        request_data_str = send_api_request(url, headers, data)

        try:
            api_response = API_Response.objects.get(request_id=request_id)
            api_response.UnsubscribeAPI_Response = request_data_str
            api_response.save()
        except API_Response.DoesNotExist:
            return HttpResponseBadRequest("API Response not found for given request_id")

        return JsonResponse({"message": "Unsubscribe API response updated successfully"})
