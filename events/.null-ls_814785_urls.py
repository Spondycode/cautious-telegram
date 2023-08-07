from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="name"),
    path("<int:year>/<str:month>/", views.home, name="name"),
    path("events", views.all_events, name="list-events"),
]
