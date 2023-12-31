from django.shortcuts import redirect, render
import calendar
from calendar import HTMLCalendar, week
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, Venue
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponse
from django.contrib import messages

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
    if request.user == event.manager:
        event.delete()
        messages.success(request, ("Event Deleted"))
        return redirect("list-events")
    else:
        messages.success(request, ("You Don't have Authorisation for That !"))
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
        request.POST or None, request.FILES or None, instance=venue
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
        )  #  put inside the curlies to pass back to the page.
    else:
        return render(request, "events/search_venues.html", {})


# Showing a single venue
def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    # Grab trhe events from that venue
    events = venue.event_set.all()
    return render(
        request,
        "events/show_venue.html",
        {"venue": venue, "venue_owner": venue_owner, "events": events},
    )


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
        form = VenueForm(request.POST, request.FILES)
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
    event_list = Event.objects.all().order_by("-event_date")
    return render(request, "events/event_list.html", {"event_list": event_list})


def admin_approval(request):
    # Get The Venues
    venue_list = Venue.objects.all()
    # Get Counts
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()

    event_list = Event.objects.all().order_by("-event_date")
    if request.user.is_superuser:
        if request.method == "POST":
            # Get list of checked box id's
            id_list = request.POST.getlist("boxes")

            # Uncheck all events
            event_list.update(approved=False)

            # Update the database
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)

            # Show Success Message and Redirect
            messages.success(request, ("Event List Approval Has Been Updated!"))
            return redirect("list-events")

        else:
            return render(
                request,
                "events/admin_approval.html",
                {
                    "event_list": event_list,
                    "event_count": event_count,
                    "venue_count": venue_count,
                    "user_count": user_count,
                    "venue_list": venue_list,
                },
            )
    else:
        messages.success(request, ("You aren't authorized to view this page!"))
        return redirect("home")


# Home page
def home(request, year=datetime.now().year, month=datetime.now().strftime("%B")):
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

    # Query the Events Model for the Date
    event_list = Event.objects.filter(
        event_date__year=year, event_date__month=month_number
    ).order_by("name")

    # Get current time
    time = now.strftime("%H:%M:%S")

    return render(
        request,
        "events/home.html",
        {
            "year": year,
            "month": month,
            "month_number": month_number,
            "cal": cal,
            "current_year": current_year,
            "time": time,
            "event_list": event_list,
        },
    )


def about(request):
    return render(request, "events/about.html", {})


# Only showing my events
def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me).order_by("name")
        return render(request, "events/my_events.html", {"events": events})
    else:
        messages.success(request, ("You can't do that"))
        return redirect("home")


# Search events


def search_events(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        events = Event.objects.filter(description__contains=searched)

        return render(
            request,
            "events/search_events.html",
            {"searched": searched, "events": events},
        )
    else:
        return render(request, "events/search_events.html", {"events": events})


# Show events in a venue
def venue_events(request, venue_id):
    # Grab the venue
    venue = Venue.objects.get(id=venue_id)
    # Grab trhe events from that venue
    events = venue.event_set.all()
    if events:
        return render(request, "events/venue_events.html", {"events": events})
    else:
        messages.success(request, ("That venue has no events for now!"))
        return redirect("admin-approval")


# Show Event
def show_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, "events/show_event.html", {"event": event})
