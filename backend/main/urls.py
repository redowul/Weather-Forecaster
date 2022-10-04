from django.urls import path
from forecaster import views

urlpatterns = [
    path("forecast", views.get_forecast),
]
