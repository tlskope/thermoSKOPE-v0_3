# Import the include function and the home_view we just created
from django.contrib import admin
from django.urls import path, include
from dataviewer.views import home_view  # Make sure this matches the location of your view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # Route for the homepage
    path('dataviewer/', include(('dataviewer.urls', 'dataviewer'), namespace='dataviewer')),  # Note the namespace
]
