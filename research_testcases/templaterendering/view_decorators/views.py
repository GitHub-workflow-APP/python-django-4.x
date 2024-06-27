from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.http import HttpResponse

# Attack Payload: curl 'http://localhost:8000/view_decorators/index_post' -X POST -d 'name=<script>alert(1)</script>'
@require_POST
def index_post(request):
    return HttpResponse("I am in index post " + request.POST.get('name')) # CWEID 80

# Attack Payload: curl 'http://localhost:8000/view_decorators/index_get?name=<script>'
@require_GET
def index_get(request):
    return HttpResponse("I am in index get " + request.GET.get('name')) # CWEID 80

# Attack Payload: curl 'http://localhost:8000/view_decorators/both' -X POST -d 'name=<script>alert(1)</script>'
@require_http_methods(['POST', 'GET'])
def both(request):
    return HttpResponse("I am in index " + request.POST.get('name')) # CWEID 80
