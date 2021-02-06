from django.contrib import admin
from django.urls import path, include

app_name = 'household'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('household.urls')),
]
