from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file_view, name='upload_file'),
    path('graph/', views.graph_view, name='graph_view'),
    # Add other URL patterns here
]
