# SQLi
-------

Our current DB (CWEID 89) support in Django is a bit questionable to me. Last and only time we worked on it is in (Django 1.x)[https://veracode.atlassian.net/wiki/spaces/RES/pages/10917825/Django+1.x+Research] with some [light testcases](https://gitlab.laputa.veracode.io/research-archive/bcreighton/djangoex1). Our python scanner and also our treatment for python language has changed drastically since :). We need to improve our support in this department and have better coverage of testcases. Also, how these SQLi APIs works thru ORM needs to be supported for this Django research... How to do it? Here are my thoughts:

1. Pick up sinks from above spec's and add it in our current real world application, probably `polls`. Our Real World Apps supports decent ORM, so just injecting in few sinks should give us good ORM based mature testcases.

2. Make sure API discussed in [raw queries](https://docs.djangoproject.com/en/4.1/topics/db/sql/#performing-raw-queries) are specc'ed above & testcased. If not, update the [Specifications.md](https://gitlab.laputa.veracode.io/research-roadmap/python-django-4.x/-/blob/main/Specifications.md) file.

3. Experiment with [QuerySet API](https://docs.djangoproject.com/en/4.1/ref/models/querysets/) with any missing sinks. Make sure every new sink is testcased.

4. Once above stuff is done, run it against local version of Python Scanner and see what we find and what we don't? What we should we be finding, but don't based on current specc's leading to FN. What we need to add to improve our support. Document it all additions/subtractions in [Specifications.md](https://gitlab.laputa.veracode.io/research-roadmap/python-django-4.x/-/blob/main/Specifications.md) file. 

5. We have currently specc'ed data coming out of Database as tainted. This is super questionable and would need to be changed. However, the APIs as part of Taint.DB could also be probable sinks... This should help in paying closer attention to certain APIs as part of bullet point 3 effort.

- Tip on how to prove a SQLi for an API:

```
# Tweak Person.objects.raw with whatever API you need to experiment.
result = Person.objects.raw("select * from user where id = " + tainted_data) # CWEID 89
for row in result:
	print(row) # Make sure there are more rows in the database other than the filtering criteria. If you get everything from the DB, its a SQLi.
```

One of the payloads which usually works with SQLite3:
```
"NULL or 'x'='x'"
```

Ref: [Flask-SQLAlchemy](https://gitlab.laputa.veracode.io/research-roadmap/python-flask-2.x/-/blob/main/research-testcases/flask-sqlalchemy-simple/getting_started.py) 


Previous Testcases around Django:
---------------------------------

- [Django 2](https://gitlab.laputa.veracode.io/research-roadmap/python-django2)
- [Django 3](https://gitlab.laputa.veracode.io/research-roadmap/python-django-3)
