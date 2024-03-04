from django.contrib import admin
from django.urls import path, include
from dataviewer.views import home_view  # Import your view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dataviewer/', include('dataviewer.urls')),
    path('', home_view, name='home'),  # Add this line for the root URL
]
