from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category
from rango.models import Page

from rango.forms import CategoryForm
from django.shortcuts import redirect


# what to show when someone visits a URL.

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order by using -.
    # Retrieve the top 5 only
    category_list = Category.objects.order_by('-likes')[:5]

    # Query the database for the top 5 most viewed pages.
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}

    # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list  # Pass most viewed pages to the template


    # Return a rendered response to send to the client.
    # the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)

def about (request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        # find a category name slug with the given name
        # .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages.
        # filter() will return a list of page objects/empty list.
        pages = Page.objects.filter(category=category)

        # add our results list to the template context under name pages.
        context_dict['pages'] = pages

        # also add the category object from database to the context dict.
        # use this in the template to verify that the category exists.
        context_dict['category'] = category

    except Category.DoesNotExist:
        # if we didn't find the specified category.
        # template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None
    
    # render the response and return it to the client.
    return render(request, 'rango/category.html', context=context_dict)

# display the Category Form and handle the posting of form data
def add_category(request):
    form = CategoryForm()

    # was HTTP request a POST? (method to send data to a server to create or update a resource)
    if request.method == 'POST': # check if the form was submitted
        form = CategoryForm(request.POST) # populate form with submitted data

        # have we been provided with a valid form?
        if form.is_valid():
            form.save(commit=True) # save new category to the database
            return redirect('/rango/') # redirect the user back to the index view
    else:
        # print the form errors to the terminal
        print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})




