from os import walk
from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime


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
        "home.html",
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
