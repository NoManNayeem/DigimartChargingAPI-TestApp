from django.contrib import admin
from .models import ChargingSDKs, Subscriber, API_Response

# Register your models here.
admin.site.register(ChargingSDKs)
admin.site.register(Subscriber)
admin.site.register(API_Response)
