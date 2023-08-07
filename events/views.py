# from os import path
from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event


def all_events(request):
    event_list = Event.objects.all()
    return render(request, "events/event_list.html", {"event_list": event_list})


def home(request, year=datetime.now().year, month=datetime.now().strftime("%B")):
    name = "David"
    # in case the month is added all in lower case. this makes it title case
    month = month.capitalize()
    # Convert month from string to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)  # make sure it is an int
    # create a calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    # get datetime
    now = datetime.now()
    current_year = now.year

    # Get current time
    time = now.strftime("%H:%M:%S")

    return render(
        request,
        "events/home.html",
        {
            "first_name": name,
            "year": year,
            "month": month,
            "month_number": month_number,
            "cal": cal,
            "current_year": current_year,
            "time": time,
        },
    )


# def about(request):
#     return (request, "events/about.html")
