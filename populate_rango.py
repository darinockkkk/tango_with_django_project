import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                    'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page

def populate():
# create lists of dictionaries containing the pages
# we want to add into each category.

# Then create a dict of dictionaries for our categories.
# it allows us to iterate through each data structure, 
# and add the data to our models.

    python_pages = [
        {'title': 'Official Python Tutorial',
        'url':'http://docs.python.org/3/tutorial/'},
        {'title':'How to Think like a Computer Scientist',
        'url':'http://www.greenteapress.com/thinkpython/'},
        {'title':'Learn Python in 10 Minutes',
        'url':'http://www.korokithakis.net/tutorials/python/'} ]

    django_pages = [
        {'title':'Official Django Tutorial',
        'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'},
        {'title':'Django Rocks',
        'url':'http://www.djangorocks.com/'},
        {'title':'How to Tango with Django',
        'url':'http://www.tangowithdjango.com/'} ]

    other_pages = [
        {'title':'Bottle',
        'url':'http://bottlepy.org/docs/dev/'},
        {'title':'Flask',
        'url':'http://flask.pocoo.org'} ]

    cats = {'Python': {'pages': python_pages},
        'Django': {'pages': django_pages},
        'Other Frameworks': {'pages': other_pages} }


# go through the cats dict, then add each category,
# and then adds all the associated pages for that category.
    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])

# Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views=0):
    #  creating model instances = 
    # to avoid duplicates, use get_or_create() 
    # to check if the entry exists in the database.
    # If it doesn’t exist, the method creates it. 
    # If it does, a reference to the specific model instance is returned

    # get_or_create() method returns a tuple of (object, created --- true or false).
    # [0] means we will only return an object 
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

# Start execution here! cuz above this point, we define
# functions; these are not executed unless we call them.

# Importing the module will not run this code; any classes or functions will
# however be fully accessible to you.
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
