from django.db import models
from django.core.validators import RegexValidator

from django.db import models

class ChargingSDKs(models.Model):
    APP_Name = models.CharField(max_length=255)
    APP_ID = models.CharField(max_length=255)
    API_Key = models.CharField(max_length=255)
    API_Secret = models.CharField(max_length=255)
    API_Password = models.CharField(max_length=255)
    redirect_url = models.URLField()
    public_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return self.APP_Name


class Subscriber(models.Model):
    Contact = models.CharField(max_length=13, unique=True, validators=[
        RegexValidator(regex='^\d{13}$', message='Contact must be a 13 digit number', code='nomatch')
    ])
    masked_msisdn = models.CharField(max_length=255, blank=True, null=True)  # New field for storing masked MSISDN

    Subscriber_Name = models.CharField(max_length=255)
    App = models.ForeignKey(ChargingSDKs, on_delete=models.CASCADE, related_name='subscription_requests')

    def __str__(self):
        return f"{self.Subscriber_Name} - {self.Contact}"

class API_Response(models.Model):
    request_id = models.CharField(max_length=255, unique=True) # New field for request_id

    ChargingAPI_Response = models.TextField()
    StatusAPI_Response = models.TextField()
    UnsubscribeAPI_Response = models.TextField()

    def __str__(self):
        return f"API Responses - {self.id}"
