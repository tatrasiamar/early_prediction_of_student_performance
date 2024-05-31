from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index/',views.index,name='index'),  # URL pattern for the index page
    path('predict/', views.predict, name='predict'), 
]

