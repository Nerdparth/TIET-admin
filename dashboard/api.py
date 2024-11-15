from ninja import NinjaAPI
from .models import Maintenance
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


app = NinjaAPI()

@app.get("/maintenance-mode")
def maintenance_mode(request):
    maintenance_status = get_object_or_404(Maintenance, id=1)
    status = maintenance_status.maintenance_mode
    return JsonResponse({"maintenance_mode" : status})
