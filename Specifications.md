---
**Note:** Latest version of this specifications is at https://veracode.atlassian.net/wiki/spaces/RES/pages/2094399515/Django+4.x
---
# Introduction:

This specification is for incrementing our current Django support to version 4.x with v4.1.5 to be the latest stable version at the start of this research effort. It is assumed [initial django support](https://veracode.atlassian.net/wiki/spaces/RES/pages/10920154/Python+Django), [Django 1.x](https://veracode.atlassian.net/wiki/spaces/RES/pages/10917825/Django+1.x+Research) & [Django 2.x](https://veracode.atlassian.net/wiki/spaces/RES/pages/10918665/Django+2.x+Research) are fully supported. This specification builds on top of it.

# Sinks:

**CWEID 80:**

[django.utils.safestring](https://docs.djangoproject.com/en/4.1/ref/utils/#module-django.utils.safestring).mark_safe(T)

[django.utils.safestring](https://docs.djangoproject.com/en/4.1/ref/utils/#module-django.utils.safestring).SafeString(T)

[django.utils.html](https://docs.djangoproject.com/en/4.1/ref/utils/#module-django.utils.html).format_html(T)


# Modeling

## XSS on Forms, Formsets and corresponding fields:

Tainted data can be marked as clean for html display (== uncleanser) in either python code or template files. We will be flagging for CWEID 80 accordingly depending on the location of such uncleansing process. 

The 1st step of the process is common irrespective of where we flag:

**Step 1:**

Identify field's of a [form](https://docs.djangoproject.com/en/4.1/ref/forms/api/#) which are either of type [CharField](https://docs.djangoproject.com/en/4.1/ref/forms/fields/#django.forms.CharField) or [EmailField](https://docs.djangoproject.com/en/4.1/ref/forms/fields/#django.forms.EmailField).

```
from django import forms

class ContactForm(forms.Form):

    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    message = forms.CharField(max_length=2000)
    no = forms.DecimalField(localize=False) # If we flag for this field in templates, its an FP. 

``` 

Ref: [Form with Taint carry fields](https://gitlab.laputa.veracode.io/research-roadmap/python-django-4.x/-/blob/main/research_testcases/templaterendering/form_field_rendering/forms.py)

### XSS in template files:

**Step 2:** 

Form filled with tainted data should be considered as a propogator. 

```
def home(request):

    form = ContactForm(request.POST) # <-- form instantiated with tainted data 
	...
	return render(request, 'home.html', 
				{'form': form, # <--- tainted form passed to template for rendering...
				'name':request.POST.get('name')} # <--- tainted data passed directly via a variable
				) 

```

Ref line 8 & 14 [Tainted Data filled form passed to template](https://gitlab.laputa.veracode.io/research-roadmap/python-django-4.x/-/blob/main/research_testcases/templaterendering/form_field_rendering/views.py)


**Step 3:** 

In the template if these taint carrying form fields are accessed using `data` or `value` [methods](https://docs.djangoproject.com/en/4.1/ref/forms/api/#methods-of-boundfield) and rendered with `safe` or `safeseq` filter, flag as XSS in the template. 

```
name : {{  name | safe  }} {#  CWEID 80 #} # <--- tainted data (variable name) directly passed thru context of render method
form:name:data : {{  form.name.data | safe }} {#  CWEID 80 #} # <---- accessing raw tainted form data and passing it thru `safe` filter.
```

Ref: [Taint Carry fields rendered](https://gitlab.laputa.veracode.io/research-roadmap/python-django-4.x/-/blob/main/research_testcases/templaterendering/form_field_rendering/templates/home.html)

**Note:** Classic `context` of a `render` method carrying tainted data (for e.g. `name` in above case) should still be flagged as XSS. 

### XSS in Python File:

**Step 2:** 

Flag for all XSS sinks listed in above section

```
def form_rendering_template(request):
	
    initial = {'name':mark_safe(request.POST.get('name')), # CWEID 80
              'email':mark_safe(request.POST.get('email')), # CWEID 80
             'message':mark_safe(request.POST.get('message')),} # CWEID 80

    form = ContactForm(data=initial)

    return render(request, 'form_rendering_template.html', {'form': form,})

```

or 

```
def post_share(request, post_id):
	form = EmailPostForm(request.POST) # <---- treat form as propogating taint
	cd = form.data # Tainted data propogated
	subject = f"{mark_safe(cd['name'])} recommends you read " # CWEID 80
	...
            

```


Ref: [formset rendering](https://gitlab.laputa.veracode.io/research-roadmap/python-django-4.x/-/blob/main/research_testcases/templaterendering/formset_rendering/views.py) & [form rendering](https://gitlab.laputa.veracode.io/research-roadmap/python-django-4.x/-/blob/main/research_testcases/templaterendering/form_rendering/views.py)

**Subclassing forms**

Form classes can be subclassed further and all above scenerios hold true. 

```
python code
------------

class PersonForm(forms.Form):
    name = forms.CharField()

class BeatleForm(PersonForm):
    haircut_type = forms.CharField()

form = BeatleForm(initial={mark_safe(tainted data) ... }) # CWEID 80
return render(request, 'simple_form_subclassing.html', {'form':form})


```

Ref: [Form subclassing](https://gitlab.laputa.veracode.io/research-roadmap/python-django-4.x/-/tree/main/research_testcases/templaterendering/form_subclass)


**Note:** We are making change from our previous approach of not treat mark_safe et al as XSS sinks and adding it in this spec's. This is in spirit of flagging flaws at the point of mitigation rather than at point of problem. This avoids huge frustration for developers to be clueless of where and how to mitigate in long and complex templates...


## `safeseq` filter in templates to be treated as XSS sink

When tainted data is rendered in a template file with a `safeseq` filter, it should be flagged for XSS. Basically `safeseq` filter is treated just like `safe` filter in Django templates.

```
views.py
--------
	safeseq_lst.append(request.POST.get('name')) # <-- tainted data is being set 
    
    return render(request, 'home.html', {'form': form,'name':request.POST.get('name'),'safeseq_lst':safeseq_lst}) # <--- safeseq_lst contains tainted data

home.html
---------
SafeSeqList : {{ safeseq_lst | safeseq | join:", "}} {# CWEID 80 #} # <--- Tainted data rendered using sqfeseq filter


```
Ref: [safeseq testcase](https://gitlab.laputa.veracode.io/research-roadmap/python-django-4.x/-/blob/main/research_testcases/templaterendering/form_field_rendering/templates/home.html#L17)



## Autoescaping shut off globally

Autoescaping can be shutoff globally for a project in it's settings.py file. Look for below pattern and flag it for CWEID 80:

```
TEMPLATES = [
...
{'autoescape':False}, # CWEID 80
]
```

Ref: [Global Shutting of autoescaping](https://gitlab.laputa.veracode.io/research-roadmap/python-django-4.x/-/blob/main/research_testcases/global_autoescaping_off/global_autoescaping_off/settings.py#L66)

Please use below custom message string for this flaw:

<span>Globally disabling of autoescaping is done thru Django settings file. This is a cross-site scripting(XSS) flaw. If the application populates the HTTP response with untrusted input, an attacker can embed malicious content, such as Javascript code, which will be executed in the context of the victim's browser.  XSS vulnerabilities are commonly exploited to steal or manipulate cookies, modify presentation of content, and compromise confidential information, with new attack vectors being discovered on a regular basis.</span> 
<span>By default autoescaping is turned on in Django. This option should never be set to False if you are rendering HTML templates. If you need escaping to be turned off, it should be done on just that particular case only after careful auditing and using contextual escaping. </span> 
<span>References: <a href="https://cwe.mitre.org/data/definitions/79.html">CWE</a> <a href="https://owasp.org/www-community/attacks/xss/">OWASP</a><a href="https://docs.djangoproject.com/en/4.1/topics/templates/#django.template.backends.django.DjangoTemplates">Global Autoescape Option</a> </span>

## [View Decorator Entry Points](https://docs.djangoproject.com/en/4.1/topics/http/decorators/)

Functions annotated with below decorators should be treated as entry points:

```
@require_POST
@require_GET
@require_http_methods
```

Ref: [View Decorator Entry Point](https://gitlab.laputa.veracode.io/research-roadmap/python-django-4.x/-/tree/main/research_testcases/templaterendering/view_decorators)

## Asynchronous Functionality

HTTP method named handler methods such as get, post, put, head, delete, options & trace with `async` keyword should be considered as valid entry points.

```

class OfferView(View):

    async def post(self, request): # <--- Entry Point
        return HttpResponse("Async Class based Views post " + request.POST.get("tainted_name"))  # CWEID 80

```

Everything specc'ed in [Django 2.x](https://veracode.atlassian.net/wiki/spaces/RES/pages/10918665/Django+2.x+Research#Django2.xResearch-IdentifyingViews) under class based views is still valid for these asynchronous views and should be supported.

**Asynchronous DB Calls**

Asynchronous DB calls are called by prepending `async for` in front of existing SQLi sinks, which we need to make sure to flag:

```
async for p in Person.objects.raw("SELECT * FROM async_db_person where name = '" + request.POST.get('search') + "'"): # CWEID 89
        ret_result += p.name + '\n'
```

Ref: [HTTP Method named handler entry points](https://gitlab.laputa.veracode.io/research-roadmap/python-django-4.x/-/blob/main/research_testcases/async_functionality/class_based_views/views.py)


# Changes to existing spec's
Sources and Sinks configured as `django.db.models.Model...(T)` in [Django 1.x](https://veracode.atlassian.net/wiki/spaces/RES/pages/10917825/Django+1.x+Research) really means object of `django.db.models.Model`. For e.g:

```
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=96)
    phone_number = models.CharField(max_length=12)

...
names = ''
for detail in Person.objects.all(): # <--- Person extends models.Model and thus is Tainted.DB source 
        names += detail.name

footer = mark_safe(names) # CWEID 80, tainted data coming from Taint.DB above <--- propagating taint to template below
....

results = Person.objects.raw("SELECT * FROM async_db_person where name = '" + request.POST.get('search') + "'")  # CWEID 89
```

Ref : [Polls real world testcase](https://gitlab.laputa.veracode.io/research-roadmap/python-django-4.x/-/blob/main/research_testcases/real_world_app_2_poll/blog/views.py#L26) & [Blog real world testcase](https://gitlab.laputa.veracode.io/research-roadmap/python-django-4.x/-/tree/main/research_testcases/real_world_app_1_blog)

-----------------
# Research ScratchPad:
Phase 1 scoped items:

```
1. Template Based Form Rendering : 
	https://docs.djangoproject.com/en/4.0/releases/4.0/#template-based-form-rendering
	https://docs.djangoproject.com/en/4.1/ref/forms/api/
	https://docs.djangoproject.com/en/4.1/topics/forms/formsets/
2. Async Database Calls
3. Async Views (we already support a whole lot of it, we need to double check, with some newer stuff if we can support out of box)
4. Better ORM support if needed
5. Re-think spec's, more testcases for our Django DB work.
```

SQLi APIs:

https://docs.djangoproject.com/en/4.1/topics/db/sql/#performing-raw-queries

ToDo for XSS:
-------------
- Setting autoescape=False in a template context

response = render(request, "index.html", {"autoescape": False})


# Reference:

- [Whats New 4.0](https://docs.djangoproject.com/en/4.0/releases/4.0/#whats-new-4-0)
- [Whats New 4.1](https://docs.djangoproject.com/en/4.1/releases/4.1/#whats-new-4-1)
- [Whats New 3.1](https://docs.djangoproject.com/en/4.1/releases/3.0/#whats-new-3-0)
- [Semgrep's Django XSS Cheatsheet](https://semgrep.dev/docs/cheat-sheets/django-xss/)