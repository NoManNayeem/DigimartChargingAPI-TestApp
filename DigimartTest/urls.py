
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # Accounts Management
    path('', include('apiexecutor.urls')),
]
