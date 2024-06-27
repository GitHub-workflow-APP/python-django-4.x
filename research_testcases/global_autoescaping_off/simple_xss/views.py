from django.shortcuts import render

# Attack Payload: curl 'http://localhost:8000/simple_xss/' -X POST -d 'tainted_name=<script>alert(2)</script>'
def home(request):
    return render(request, 'home.html', {'tainted_name':request.POST.get('tainted_name')})