from django.urls import path
from .views import HomeView, AppView, SubscribeView
from .views import StatusAPIView, UnsubscribeAPIView



urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    
    
    
    path('<str:app_name>/', AppView.as_view(), name='app-view'),
    path('<str:app_name>/<str:phone>/', SubscribeView.as_view(), name='subscribe'),
    
    path('status/<str:app_name>/<str:phone>/', StatusAPIView.as_view(), name='status-api'),
    path('unsubscribe/<str:app_name>/<str:phone>/', UnsubscribeAPIView.as_view(), name='unsubscribe-api'),


]
