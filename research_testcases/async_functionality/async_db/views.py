from django.http import HttpResponse
from .models import Person
from .forms import SubscribeForm
from django.db import connection


async def add_person(request):

    form = SubscribeForm(request.POST)
    p = form.save()

    return HttpResponse("Added data " + request.POST.get('name')) # CWEID 80

# Attack Payload: curl 'http://localhost:8000/async_db/search' -X POST -d "search=NULL' or 'x'='x"
async def search(request):
    ret_result = "\nSQLi 1"
    results = Person.objects.raw("SELECT * FROM async_db_person where name = '" + request.POST.get('search') + "'")  # CWEID 89
    for result in results:
        ret_result += result.name + '\n'

    ret_result += "\nSQLi 2"
    with connection.cursor() as cursor:
        # This is already a TP. We flag this
        cursor.execute("SELECT * from async_db_person where name = '" + request.POST.get('search') + "'") # CWEID 89
        results = cursor.fetchall()
    for row in results:
        ret_result += row[1] + '\n'

    ret_result += "\nSQLi 3"
    async for p in Person.objects.raw("SELECT * FROM async_db_person where name = '" + request.POST.get('search') + "'"): # CWEID 89
        ret_result += p.name + '\n'

    ret_result += "\n SQLi 4"
    results = Person.objects.raw("SELECT * FROM async_db_person where name = '%s'" % request.POST.get('search')) # CWEID 89
    for row in results:
        ret_result += row.name

    ret_result += "\nSQLi 5"
    with connection.cursor() as cursor:
        # Already TP
        cursor.execute("SELECT * from async_db_person where name = '%s'" % request.POST.get('search')) # CWEID 89
        results = cursor.fetchall()
    for row in results:
        ret_result += row[1] + "\n"

    ret_result += "\nSQLi 6"
    with connection.cursor() as cursor:
        # TP
        cursor.execute("SELECT * from async_db_person where name = '{}'".format(request.POST.get('search'))) # CWEID 89
        results = cursor.fetchall()
    for row in results:
        ret_result += row[1] + "\n"

    ret_result += "\nSQLi 7"
    with connection.cursor() as cursor:
        # TP
        cursor.execute(f"SELECT * from async_db_person where name = '{request.POST.get('search')}'") # CWEID 89
        results = cursor.fetchall()
    for row in results:
        ret_result += row[1] + "\n"


    ret_result += "\nSQLi 8"
    results = Person.objects.raw("SELECT * FROM async_db_person where name = %s" % request.POST.get('search')) # CWEID 89
    for row in results:
        ret_result += row.name


    ret_result += "\nSQLi 9"
    results = Person.objects.raw("SELECT * FROM async_db_person where name = '%s'" % [request.POST.get('search')]) # FP CWEID 89
    for row in results:
        ret_result += row.name

    ret_result += "\nSQLi 10"
    with connection.cursor() as cursor:
        # We are flagging this
        cursor.execute(f"SELECT * FROM async_db_person where name = '%s'" % [request.POST.get('search')]) # FP CWEID 89
        results = cursor.fetchall()
    for row in results:
        ret_result += row[1] + "\n"

    print(ret_result)

    return HttpResponse("Searched data : " + ret_result) # CWEID 80
