# from os import path
from django.shortcuts import redirect, render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, Venue
from .forms import VenueForm, EventForm


# The update venues thing
def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(
        request.POST or None, instance=event
    )  # instance brngs in the details from the database entry
    if form.is_valid():
        form.save()
        return redirect("list-events")
    return render(request, "events/update_event.html", {"event": event, "form": form})


# Add the Event page
def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/add_event?submitted=True")
    else:
        form = EventForm
        if "submitted" in request.GET:
            submitted = True
    return render(
        request, "events/add_event.html", {"form": form, "submitted": submitted}
    )


# The update venues thing
def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(
        request.POST or None, instance=venue
    )  # instance brngs in the details from the database entry
    if form.is_valid():
        form.save()
        return redirect("list-venues")
    return render(request, "events/update_venue.html", {"venue": venue, "form": form})


# Searching the venues
def search_venues(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        venues = Venue.objects.filter(
            name__contains=searched
        )  # To make the search of the database
        return render(
            request,
            "events/search_venues.html",
            {"searched": searched, "venues": venues},
        )  # inside the curlies to pass back to the page.
    else:
        return render(request, "events/search_venues.html", {})


# Showing a single venue
def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request, "events/show_venue.html", {"venue": venue})


# List all the venues
def list_venues(request):
    venue_list = Venue.objects.all()
    return render(request, "events/venues.html", {"venue_list": venue_list})


# Add a venue
def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/add_venue?submitted=True")
    else:
        form = VenueForm
        if "submitted" in request.GET:
            submitted = True
    return render(
        request, "events/add_venue.html", {"form": form, "submitted": submitted}
    )


# List all the events
def all_events(request):
    event_list = Event.objects.all()
    return render(request, "events/event_list.html", {"event_list": event_list})


# Home page
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
