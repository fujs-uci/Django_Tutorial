# Django-Tutorial: Writing your first Django App
- A summary of Django Tutorial. 
- Skips over [installation](https://www.djangoproject.com/download/)
- Based on Windows system. 
- Using MySQL database
- Changed Class, Function, and Variable names to [TYPE].

## Part 1: Project, Development Server, App, and View

### Creating Project
Project is a collection of configurations and Apps. 

Go into a desired directory and type in CMD:
```
$ django-admin startproject [PROJECT]
```
Creates directory:
```
[PROJECT]/                      # outer [PROJECT] doesn't matter
    manage.py                   # Admin controls here
        [PROJECT]/              # inner [PROJECT] refereced for packages
            __init__.py     
            settings.py         # Security, Debug, Config
            urls.py             # Config URL patterns, table of contents
            wsgi.py             # Deployment to web servers, initially local
```
### Running Development server
Inside outer [PROJECT] path , type in CMD:
```
$ python manage.py runserver 8000      # http://127.0.0.1:8000/
                                       # port = 8000
                                       # Automatically reloads code changes, New files need restart
                                       # Host for Django Project
```
### Creating First App in project
App is a Web application & can be in multiple projects.

Inside outer [PROJECT] path, type in CMD:
```
$ Python manage.py startapp [APPNAME]
```
Creates directory:
```
[APPNAME]/        # directory to house [APPNAME] application
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```
### Creating First View
Inside [APPNAME]/views.py, add in code:
```
from django.http import HTTpResponse

def [VIEWNAME1](request):
    return HttpResponse("Hello, world1. You're at the [APPNAME] [VIEWNAME1] web page.")
```
Create a [APPNAME]/urls.py file and add in code:
```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.[VIEWNAME1], name='[VIEWNAME1]'),
]
```
Inside [PROJECT]/urls.py, add in code:
```
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('[APPNAME]/', include('[APPNAME].urls')),      # include() references other urls.py
    path('admin/', admin.site.urls),                    # path(route, view, kwarges, name) 
]                                                       #   route = [WEBSITE].com/[ROUTE]/... 
                                                        #   name = allows unambiguous referecing
```
## Part 2: Database, Models, API, Admin

### Setup DataBase
Inside [PROJECT]/settings.py update code:
```
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     [DATABASE NAME],
        'USER':     [USER],
        'PASSWORD': [PASSWORD],
        'HOST':     "127.0.0.1",                # Local Machine
        'PORT':     "3306",
    }
}
```
Create necessary Database tables with migrate command. This is the initial call when first creating the Project.

Inside outer [PROJECT] path , type in CMD:
```
$ python manage.py migrate      # Looks at INSTALLED_APPS in [PROJECT]/settings.py
```
### Creating Models
Models define the data's fields abd behaviors. Represents MySQL's create table.

Inside [APPNAME]/models.py add in code for Models:
```
class [MODELNAME](models.Model):
    [TEXTFIELD]     = models.CharField(max_length=200)
    [DATEFIELD]     = models.DateTimeField('date published')
    [INTEGERFIELD]  = models.IntegerField(default=0)
    [FOREIGNKEY]    = models.ForeignKey([OTHERMODEL], on_delete=models.CASCADE)
```
### Activating Models
Django Apps are "pluggable" to multiple projects, must be activated after creation

Inside [PROJECT]/settings.py, add into INSTALLED_APPS:
```
INSTALLED_APPS = [
    '[APPNAME].apps.[APPNAME]sConfig',
    ...
]
```
Steps for making model changes:
1. Update models.py
2. makemigrations
3. migrate

Inside outer [PROJECT] path , type in CMD:
```
$ python manage.py makemigrations [APPNAME]     # Creates code to update Database
                                                #   - [APPNAME]/migrations/XXXX_initial.py

$ python manage.py sqlmigrate [APPNAME] XXXX    # refers to code created by makemigrations
                                                # generates a file with sql code

$ python manage.py check                        # debug's project before migrations

$ python manage.py migrate                      # Updates to Database are executed
```

### Playing with the API
Django has a built-in database API.

Access to [MODEL] objects by calling on the Database
```
from [APPNAME].models import [MODEL]
[MODEL].objects.all()                       # Displays all [MODEL] data entries
```

Single [MODEL] object api calls. 

>[Model relations](https://docs.djangoproject.com/en/2.1/ref/models/relations/)

>[Field lookups](https://docs.djangoproject.com/en/2.1/topics/db/queries/#field-lookups-intro)
```
firstModel = [MODEL]([FIELDNAME] = 'old')   # Initializes a [MODEL] data
firstModel.save()                           # Saves instance to Database, must be explicitly called
firstModel.id                               # unique id auto generated
firstModel.[FIELDNAME]                      # returns the value of the [FIELDNAME]
firstModel.[FIELDNAME] = 'new'
firstModel.save()                           # Must be called to finalize change
[MODEL].objects.filter(id=X)                # .filter() is a query based on key words
getModel = [MODEL].objects.get(pk=X)        # Gets an existing [MODEL] data
```
### Django Admin
Creating an Admin User:

Inside outer [PROJECT] path , type in CMD:
```
$ python manage.py createsuperuser          # prompt user for username, emai, & password
```
Access to admin on Local server: http://127.0.0.1:8000/admin/

Allow Admin to modify Apps and add an Admin App interface, in [APPNAME]/admin.py add code:
```
from django.contrib import admin
from .models import [MODEL]

admin.site.register([MODEL])
```

## Part 3: Views, More Views, Errors, Templates, & URLs
Views relate to the public interface. Each view is relates to a unique web pages with specific functions and templates. Webpages and content are delivered by views. Views return HttpResponse Objects containing content for the page or raising exceptions.

### Writing more Views
Inside of [APPNAME]/views.py, new views are new functions:
```
def [VIEWNAME2](request, args):
    return HttpResponse("2", args)
    
def [VIEWNAME3](request, args):
    return HttpResponse("3", args)    
    
def [VIEWNAME4](request, args):
    return HttpResponse("4", args)    
```
Inside of [APPNAME]/urls.py, add new path() for each view:
```
from . import views
urlpatterns = [
    path('', views.[VIEWNAME1], name = '[VIEWNAME1]')                       # URL = [WEBSITE].com/[APPNAME]/
    path('<[ARGS]>/', views.[VIEWNAME2], name = '[VIEWNAME2]')              # URL = [WEBSITE].com/[APPNAME]/[ARGS]/
    path('<[ARGS]>/[VIEWNAME3]/', views.[VIEWNAME3], name = '[VIEWNAME3]')  # URL = [WEBSITE].com/[APPNAME]/[ARGS]/[VIEWNAME3]/
    path('<[ARGS]>/[VIEWNAME4]/', views.[VIEWNAME4], name = '[VIEWNAME4]')  # URL = [WEBSITE].com/[APPNAME]/[ARGS]/[VIEWNAME4]/
]
```
### Write views that actually do something

Example view with hard-coded page design:
```
def [VIEWNAME1](request):
    result_list = [MODEL].objects.order_by('[FIELDNAME]')[:5]
    result = ','.join(list(x.[FIELDNAME] for x in result_list))
    return HttpResponse(result)
```
Inside [APPNAME] directory, create a templates directory:
```
[APPNAME]/
    templates/                       
        [APPNAME]/                  # Needs to share the same name
            [TEMPLATENAME1].html    # Html code with {%%} expressions and {{}} variable outputs
    ...
```
Redesign of example view with template design:
```
from django.template import loader

def [VIEWNAME1](request):
    result_list = [MODEL].objects.order_by('[FIELDNAME]')[:5]
    context = {'result_list': result_list, }
    template = loader.get_template('[APPNAME]/[TEMPLATENAME1].html')
    return HttpResponse(template.render(context, request))
```
Redesign of example view with render():
```
from django.shortcuts import render

def [VIEWNAME1](request):
    result_list = [MODEL].objects.order_by('[FIELDNAME]')[:5]
    context = {'result_list': result_list}
    template = '[APPNAME]/[TEMPLATENAME1].html'
    return render(request, template, context)
```

### Raising 404 Error
Instead of a try except block, use get_object_or_404() or get_list_or_404():
```
from django.shortcuts import get_object_or_404, render

def [VIEWNAME1](request, question_id):
    result = get_object_or_404([MODEL], pk=[MODEL]_id)        # get_list_or_404([MODEL], pk=[MODEL]_id) 
    template = '[APPNAME]/[TEMPLATENAME1].html'
    return render(request, template, {'result': result})
```

### Use the Template System
Check template guide:
>  [Templates](https://docs.djangoproject.com/en/2.1/topics/templates/)

Templates use HTML. 2 important features of templates:
1. '{{}}' denote python variables or objects e.g. {{ [MODEL].[FIELDNAME] }}
2. '{%%}' denote python method calling e.g. {% for [MODEL] in [MODEL].objects.all() %}

### Removing Hardcoded URLs in templates
Hard-coded links:
```
<li><a href="
    /[APPNAME]/{{ [MODEL].[FIELDNAME1] }}/">        # Update template to change url
    {{ [MODEL].[FIELDNAME2] }}
</a></li>
```
Using {% url %} tag as listed in [APPNAME]/urls.py:
```
<li><a href=
    "{% url [NAME] [MODEL].[FIELDNAME1] %}">        # Update path(url, view, [NAME]) to change url
    {{ [MODEL].[FIELDNAME2] }}
</a></li>
```
### Namespacing URL names
Adding Namespaces to differentiate same named views in different Apps.

Inside [APPNAME]/urls.py add in code:
```
app_name = '[APPNAME]'              # declares namespace
urlpatterns = [...]
```
Update [APPNAME]/[TEMPLATENAME1].html with app_name namespace:
```
<li><a href=
    "{% url app_name:[NAME] [MODEL].[FIELDNAME1] %}">     
    {{ [MODEL].[FIELDNAME2] }}
</a></li>
```
## Part 4:
### Simple Form
Inside [APPNAME]/template/[APPNAME]/[TEMPLATENAME1].html add in code:
```
<form action=
    "{% url '[APPNAME]:[VIEW]' [MODEL].[FIELDNAME1] %}" 
method="post">
{% csrf_token %}                                                    # Django built-in security
{% for choice in [MODEL].[RELATEDMODEL]_set.all %}                  # [MODEL].[RELATEDMODEL]_set = Relation managment
    <input  type="radio" 
            name="choice"                                           # Will be refered in view as Post[name] dict
            id="[RELATEDMODEL]{{ forloop.counter }}"                # forloop.counter = built-in counter
            value="{{ [RELATEDMODEL].[FIELDNAME1] }}">
            
    <label for="[RELATEDMODEL]{{ forloop.counter }}">
            {{ [RELATEDMODEL].[RELATEDMODEL]_[FIELDNAME2] }}        # Another relation mangement
            </label><br>
{% endfor %}
<input type="submit" value="Vote">
</form>
```
Inside [APPNAME]/views.py update [VIEW] function:
```
def [VIEW2](request, args):
    model_object = get_object_or_404([MODEL], pk=[MODEL]_[FIELDNAME1])
    try:
        selected_model = [MODEL].[RELATEDMODEL]_set.get(pk=request.POST['choice'])      # refers to template <input> name.
    except (KeyError, [RELATEDMODEL].DoesNotExist):                 
        return render(request, '[APPNAME]/[TEMPLATENAME2].html', {
            'model_object': model_object,
            'error_message': "some error",
        })
    else:
        selected_model.[FIELDNAME1] += 1
        selected_model.save()
        redir = reverse(  '[APPNAME]:[TEMPLATENAME2]',                  # redir = [APPNAME]/[MODEL].[FIELDNAME]/[TEMPLATENAME2]
                                args=([MODEL].[FIELDNAME],))
        return HttpResponseRedirect( redir )                            # HttpResponseRedirect used for POST data
```
Consider using F() for race conditions:
>[Race COnditions](https://docs.djangoproject.com/en/2.1/ref/models/expressions/#avoiding-race-conditions-using-f)

### Generic Views, less is better
Creating generic views for templates with similar functions:
1. Convert URLconf
2. Delete old, unneeded views
3. Create new views based on Django generic views
>[Generic Views](https://docs.djangoproject.com/en/2.1/topics/class-based-views/)

Inside [APPNAME]/urls.py, ammend the URLconf:
```
app_name = '[APPNAME]'
urlpatterns = [
    path('', views.[VIEWNAME1].as_view(), name = '[VIEWNAME1]')                         # added .as_view()
    path('<int:pk>/', views.[VIEWNAME2].as_view(), name = '[VIEWNAME2]')                # changed [ARGS] to <int:pk> for DetailView
    path('<int:pk>/[VIEWNAME3]/', views.[VIEWNAME3].as_view(), name = '[VIEWNAME3]') 
    path('<[ARGS]>/[VIEWNAME4]/', views.[VIEWNAME4], name = '[VIEWNAME4]') 
]
```
Inside [APPNAME]/views.py, ammend the views:
```
from django.views import generic

class [VIEWNAME1](generic.ListView):                                # generic.ListView = display a list of objects
    template_name = '[APPNAME]/[TEMPLATENAME1].html'
    context_object_name = 'latest_result_list'

    def get_queryset(self):
        return [MODEL].objects.order_by('-[FIELDNAME1]')[:5]

class [VIEWNAME2](generic.DetailView):                              # generic.DetailView = display details of a specific object
    model = [MODEL]
    template_name = '[APPNAME]/[TEMPLATENAME2].html'

class [VIEWNAME3](generic.DetailView):
    model = [MODEL]
    template_name = '[APPNAME]/[TEMPLATENAME3].html'
```
## Part 5:
>[Testing in Django](https://docs.djangoproject.com/en/2.1/topics/testing/)
### Automated testing
Having tests is good:
1. Saves time from debugging
2. Identify AND prevent bugs
3. Tests are sexy
4. Integrates code variation
### Basic Testing Strategies
Convert requirements into test cases, then code:
>[Test-driven Development](https://en.wikipedia.org/wiki/Test-driven_development)
### First Test
Identify possible bugs, example bug:
```
modelDate = pub_date=timezone.now() + datetime.timedelta(days=30)   # set 30 dats in future
future_model = [MODEL](modelDate)
future_model.was_published_recently()                               # returns True, but recent != future
```
Expose the bug. Inside [APPNAME]/tests.py add code:
```
from django.test import TestCase

class modelModelTests(TestCase):
    def test_was_published_recently_with_future_model(self):                # Write testcase for all edge cases
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)      # Error in .was_published_recently()
```
Running tests on specific Apps, type in CMD:
```
$ python manage.py test [APPNAME]       # Will display info on failed/passed tests
```
### Test a view
Testing behavior is experience uniformly by back-end and front-end.

Testing views inside [APPNAME]/tests.py:
```
class [TESTVIEW1](TestCase):
    def test1(self):
        response = self.client.get(reverse('[APPNAME]:[VIEW]'))
        self.assertEqual(response.status_code, 200)                     # assertEqual
        self.assertContains(response, "Empty.")                         # assertContains
        self.assertQuerysetEqual(response.context['...'], [])           # assertQuerysetEqual
    def test2(self):
        ...
```
### More testing is better
Simple guide-line:
1. Have seperate Testcase for each model or view
2. Separate test method for each condition or requirment
3. Test method names that describe the function
## Part 6:
Images, Javascript, and CSS are refered as "static files". django.contrib.staticfiles centralizes all static files from different locations

>[Static files howto](https://docs.djangoproject.com/en/2.1/howto/static-files/)

>[Static files referece](https://docs.djangoproject.com/en/2.1/ref/contrib/staticfiles/)

>[Deploying Static files](https://docs.djangoproject.com/en/2.1/howto/static-files/deployment/)

### Font-end: Look and feel
Inside [APPNAME] directory, create a static firectory:
```
[APPNAME]/
    static/                         # Same format as template directory
        [APPNAME]/
            images/
                [IMAGE1].jpeg
            [STATIC1].css
            [STATIC2].css
```
To reference static files, inside template/[APPNAME]/[TEMPLATENAME1].html, add:
```
{% load static %}
<link rel="stylesheet" type="text/css" href="{% static '[APPNAME]/[STATIC1].css' %}">
```
### Background image
Inside a .css file, add:
```
body {
    background: white url("images/[IMAGE1].jpeg") no-repeat;
}
```
## Part 7:
### Customize Admin
Django admin creates a default interface. To customize add this code to [APPNAME]/admin.py:
```
from django.contrib import admin

class myModelAdmin(admin.ModelAdmin):
    fields = ['[FIELDNAME1]', '[FIELDNAME2]']           # Change switches the display ordering of fields    

admin.site.register([MODEL], myModelAdmin)
```
Adding field sets, like headers and subheaders:
```
class myModelAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['[FIELDNAME1]']}),     # Header = 
        ('Date information', {'fields': ['[FIELDNAME2]']}),     # Header = Date information
    ]
```
### Adding Related Objects
Registerign a [RELATEDMODEL], add code inside [APPNAME]/admin.py:
```
admin.site.register([RELATEDMODEL])         # related models are foreign keys
```
Add [RELATEDMODEL] when creating a new [MODEL]. Inside [APPNAME]/admin.py:
```
class RelatedModelInline(admin.StackedInline):                  # admin.StackedInline or admin.TabularInline
    model = [RELATEDMODEL]
    extra = 3                                                   # At least 3 [RELATEDMODEL] per [MODEL]

class myModelAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['[FIELDNAME1]']}),
        ('Date information', {'fields': ['[FIELDNAME2]'], 
                              'classes': ['collapse']}),
    ]
    inlines = [RelatedModelInline]                              # [RELATEDMODEL] objects edited on [MODEL] page

admin.site.register([MODEL], myModelAdmin)
```
### Admin Change list
Add more information to be displayed for [MODEL]. Inside [APPNAME]/admin.py:
```
class myModelAdmin(admin.ModelAdmin):
    ...
    list_display([FIELDNAME1], [FIELDNAME2], [MODELMETHOD1])
```
Allow sorting of [MODEL] methods, inside [APPNAME]/models.py:
```
class [MODEL](models.Model):
    def [MODELMETHOD1](self):
        ...
    [MODELMETHOD1].admin_order_field = '[FIELDNAME1]'
    [MODELMETHOD1].boolean = True
    [MODELMETHOD1].short_description = '...'
```
Add filter sidebar and basic LIKE search, [APPNAME]/admin.py:
```
class myModelAdmin(admin.ModelAdmin):
   ...
   list_filter = ['[FIELDNAME1]']
   search_fields = ['[FIELDNAME1]']
```
### Admin Front-end
Admin templates can be customized.
>[Template Loading](https://docs.djangoproject.com/en/2.1/topics/templates/#template-loading)

Create a admin templates directory inside [PROJECT] directory:
```
[PROJECT]/
    templates/
        admin/                                                  # Admin templates to override
            base_site.html                                      #   ^
            index.html                                          #   ^
        manage.py 
```
Inside [PROJECT]/settings.py add code:
```
TEMPLATES = [
    {
        'DIRS': [os.path.join(BASE_DIR, 'templates')],          # search path when loading Django templates
        ...}
]
```
Find default Django admin templates
```
$ python -c "import django; print(django.__path__)"             # django.contrib.admin.templates
```
## Final Directory
```
[PROJECT]/
    manage.py
    [PROJECT]/
        __init__.py
        settings.py
        urls.py
        wsgi.py
    [APPNAME1]/
        __init__.py
        admin.py
        migrations/
            __init__.py
            0001_initial.py
        models.py
        static/
            [APPNAME1]/
                images/
                    background.gif
                style.css
        templates/
            [APPNAME1]/
                [TEMPLATENAME1].html
                [TEMPLATENAME2].html
                [TEMPLATENAME3].html
        tests.py
        urls.py
        views.py
    templates/
        admin/
            base_site.html
```
