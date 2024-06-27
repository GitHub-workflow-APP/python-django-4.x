import asyncio

from django.http.response import HttpResponse
from django.views.generic import View
from django.utils.decorators import classonlymethod


class OfferView(View):

    # Attack Payload: curl 'http://localhost:8000/class_based_views/offer' -X POST -d 'tainted_name=<script>alert(1)</script>'
    async def post(self, request):
        return HttpResponse("Async Class based Views post " + request.POST.get("tainted_name"))  # CWEID 80

    # Attack Payload: curl 'http://localhost:8000/class_based_views/offer?tainted_name=<script>alert(1)</script>' -X GET
    async def get(self, request):
        return HttpResponse("Async Class based Views get " + request.GET.get("tainted_name"))  # CWEID 80

    # Attack Payload: curl 'http://localhost:8000/class_based_views/offer?tainted_name=<script>alert(1)</script>' -X GET
    async def head(self, request):
        return HttpResponse("Async Class based Views head " + request.GET.get("tainted_name"))  # CWEID 80

    # Attack Payload: curl 'http://localhost:8000/class_based_views/offer?tainted_name=<script>alert(1)</script>' -X PUT
    async def put(self, request):
        return HttpResponse("Async Class based Views put " + request.GET.get("tainted_name"))  # CWEID 80

    # Attack Payload: curl 'http://localhost:8000/class_based_views/offer?tainted_name=<script>alert(1)</script>' -X PUT
    async def delete(self, request):
        return HttpResponse("Async Class based Views delete " + request.GET.get("tainted_name"))  # CWEID 80

    # Attack Payload: curl 'http://localhost:8000/class_based_views/offer?tainted_name=<script>alert(1)</script>' -X OPTIONS
    async def options(self, request):
        return HttpResponse("Async Class based Views options " + request.GET.get("tainted_name"))  # CWEID 80

    # Attack Payload: curl 'http://localhost:8000/class_based_views/offer?tainted_name=<script>alert(1)</script>' -X TRACE
    async def trace(self, request):
        return HttpResponse("Async Class based Views trace " + request.GET.get("tainted_name"))  # CWEID 80
