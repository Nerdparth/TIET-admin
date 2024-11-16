from django.shortcuts import render, redirect
from .models import Maintenance
from django.shortcuts import get_object_or_404
import httpx
from django.contrib import messages
from django.http import HttpResponse


def dashboard_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    count_response = httpx.get(
        "https://smart-campus-tiet-production.up.railway.app/api/book-count"
    )
    books_count = count_response.json()
    budget_getter = httpx.get(
        "https://smart-campus-tiet-production.up.railway.app/api/get-budget"
    )
    budget = budget_getter.json()

    requests = httpx.get(
        "https://smart-campus-tiet-production.up.railway.app/api/get-all-future-books"
    )
    all_requests = requests.json()

    if request.method == "POST":
        if "add_book_form" in request.POST:
            book_name = request.POST["book_name"]
            author_name = request.POST["book_author"]
            book_quantity = request.POST["book_quantity"]
            data_to_add_book = {
                "book_name": book_name,
                "author": author_name,
                "quantity": book_quantity,
            }
            add_a_book = httpx.post(
                "https://smart-campus-tiet-production.up.railway.app/api/add-bought-item",
                json=data_to_add_book,
            )
            messages.success(request, "book added successfully")

        if "update_budget_form" in request.POST:
            updated_budget = request.POST["updated-budget"]
            data_to_update_budget = {"Budget": updated_budget}
            update = httpx.post(
                "https://smart-campus-tiet-production.up.railway.app/api/edit-budget",
                json=data_to_update_budget,
            )
            messages.success(request, "budget updated successfully")

        if "delete_book_form" in request.POST:
            delete_book_name = request.POST["delete-book-name"]
            delete_book_author = request.POST["delete-book-author"]
            delete_book_data = {
                "book_name": delete_book_name,
                "author": delete_book_author,
            }
            delete_book = httpx.post(
                "https://smart-campus-tiet-production.up.railway.app/api/delete-book",
                json=delete_book_data,
            )
            messages.success(request, "book deleted from db")

        if "accept_request_form" in request.POST:
            book_name = request.POST["book_name"]
            author_name = request.POST["author_name"]
            update_status = {"status": "approved"}
            update_status = httpx.post(
                f"https://smart-campus-tiet-production.up.railway.app/api/update-status/{author_name}/{book_name}",
                json=update_status,
            )

        if "reject_request_form" in request.POST:
            book_name = request.POST["book_name_reject"]
            author_name = request.POST["author_name_reject"]
            update_status = {"book_name": book_name, "author": author_name}

            update_status = httpx.post(
                f"https://smart-campus-tiet-production.up.railway.app/api/delete-future-book",
                json=update_status,
            )

    return render(
        request,
        "library.html",
        {"count": books_count, "budget": budget, "requests": all_requests},
    )


def events_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    events = httpx.get(
        "https://smart-campus-tiet-production.up.railway.app/events-api/events-count"
    )
    events_count = events.json()

    delete_events_list_getter = httpx.get(
        "https://smart-campus-tiet-production.up.railway.app/events-api/get-all-events"
    )
    delete_events_list = delete_events_list_getter.json()

    if request.method == "POST":
        if "create_event_form" in request.POST:
            event_name = request.POST["create_event_name"]
            event_host = request.POST["create_event_host"]
            event_date = request.POST["create_event_date"]
            event_description = request.POST["create_event_description"]
            data = {
                "event_name": event_name,
                "description": event_description,
                "hosted_by": event_host,
                "datetime": event_date,
            }
            create_event = httpx.post(
                "https://smart-campus-tiet-production.up.railway.app/events-api/add-event",
                json=data,
            )

        if "delete_event_form" in request.POST:
            delete_event_name = request.POST["delete_event"]
            delete_event_data = {"event_name": delete_event_name}
            delete_event = httpx.post(
                "https://smart-campus-tiet-production.up.railway.app/events-api/delete-event",
                json=delete_event_data,
            )

    return render(
        request,
        "events.html",
        {"count": events_count, "delete_event_list": delete_events_list},
    )


def maintenance_view(request):
    maintenance = get_object_or_404(Maintenance, id=1)
    if request.method == "POST":
        maintenance_mode = "maintenance" in request.POST
        maintenance.maintenance_mode = maintenance_mode
        maintenance.save()

    return render(
        request, "maintenance.html", {"maintenance": maintenance.maintenance_mode}
    )


def attendee_list(request, event_name: str):
    try:
        response = httpx.get(
            f"https://smart-campus-tiet-production.up.railway.app/events-api/get-all-attendees/{event_name}"
        )
        response.raise_for_status()  # Raises an HTTPError for non-200 responses
        attendees = response.json()  # Attempt to parse JSON
    except httpx.RequestError as e:
        print(f"Request error: {e}")
        return HttpResponse("Error fetching attendees", status=500)
    except ValueError as e:
        print(f"JSON decode error: {e}")
        attendees = []  # Fallback to an empty list if JSON is invalid

    return render(request, "attendee.html", {"attendees": attendees})
