from django.contrib import admin
from django.urls import path
from authentication.views import login_view
from dashboard.views import dashboard_view, events_view, maintenance_view, attendee_list
from dashboard.api import app


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login", login_view, name="login"),
    path("", dashboard_view, name="dashboard"),
    path("events/", events_view, name="events"),
    path("api/", app.urls),
    path("maintenance/", maintenance_view, name="settings"),
    path("attendee/<str:event_name>", attendee_list, name="attendees"),
]
