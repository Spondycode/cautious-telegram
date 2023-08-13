from django.shortcuts import redirect, render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, Venue
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponse

# import pagination dependencies
from django.core.paginator import Paginator


# Generate a text file
def venue_text(request):
    response = HttpResponse(content_type="text/plain")
    response["content-Disposition"] = "attachment; filename=venues.txt"
    # Designate the models
    venues = Venue.objects.all()

    lines = []
    # loop through them
    for venue in venues:
        lines.append(f"{venue}\n{venue.address}\n{venue.phone}\n\n")

    # Write to text file
    response.writelines(lines)
    return response


# Delete Venue
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect("list-venues")


# Delete Event
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect("list-events")


# The update venues thing
def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
    # instance brngs in the details from the database entry
    if form.is_valid():
        form.save()
        return redirect("list-events")
    return render(request, "events/update_event.html", {"event": event, "form": form})


# Add the Event page
def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/add_event?submitted=True")
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                # form.save()
                event = form.save(commit=False)
                event.manager = request.user  # logged in User
                event.save()
                return HttpResponseRedirect("/add_event?submitted=True")

    else:
        # Just going to the page - Not Submitting
        if request.user.is_superuser:
            form = EventFormAdmin
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

    # Set up pagination
    p = Paginator(Venue.objects.all(), 3)
    page = request.GET.get("page")
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages
    return render(
        request,
        "events/venues.html",
        {"venue_list": venue_list, "venues": venues, "nums": nums},
    )


# Add a venue
def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            # form.save()
            venue = form.save(commit=False)
            venue.owner = request.user.id  # Logged in User
            venue.save()
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
    event_list = Event.objects.all().order_by("name")
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
