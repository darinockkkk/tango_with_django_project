from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category
from rango.models import Page

from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm

from django.shortcuts import redirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from datetime import datetime

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
    context_dict['pages'] = page_list  # Pass most viewed pages to the templat

    visitor_cookie_handler(request)

    # return response back to user, updating any cookies that need changed
    return render(request, 'rango/index.html', context=context_dict)

# helper function
# all cookies are stored server-side, so we can remove response from visitor_cookie_handler() definition
# asks request for cookie. If it's is in session data, then its value is returned
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# helper function
# we access incoming cookies from request
# all cookie values are returned as strings
def visitor_cookie_handler(request):
    # get number of visits to site - use COOKIES.get() to obtain visits cookie
    # if cookie doesn't exist, value of 1 is used
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    
    # if more than a day since last visit
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # update last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # set last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # update visits cookie ('<cookie_name>', value)
    request.session['visits'] = visits

def about (request):
    print(request.method) #GET or POST
    print(request.user) # user status

    context_dict = {}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/about.html', context=context_dict)
    # return response back to user, updating any cookies that need changed
    return response

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

@login_required
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

@login_required
def add_page(request, category_name_slug):
    
    # you cant add a page to Category that doesnt exist
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    if category is None:
        # redirect the user back to the index page
        return redirect('/rango/')

    form = PageForm()

    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False) # create a Page object but don't save it yet
                page.category = category # assign the page to the correct category
                page.views = 0
                page.save() # save the page to the database

                # redirect user to category page after adding a new page

                # reverse() generates URL for show_category view
                # 'rango:show_category' refers to the URL name in urls.py
                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug': category_name_slug})) # fill in URL parameter (category_name_slug)
        
        else:
            print(form.errors)

    # when form is not submitted or invalid
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

#def register(request):
#    registered = False
#
#    if request.method == 'POST':
#        # initializes a form with user credentials + with additional user profile details
#        user_form = UserForm(request.POST)
#        profile_form = UserProfileForm(request.POST)
#
#        if user_form.is_valid() and profile_form.is_valid():
#            # save user's form data to database
#            user = user_form.save()
#
#            # hash password with set_password method
#            user.set_password(user.password)
#            # update user object
#            user.save()
#
#            # prevents saving immediately (needed cuz UserProfile must be linked to User first)
#            profile = profile_form.save(commit=False)
#            # links the UserProfile to the corresponding User
#            profile.user = user
#
#            if 'picture' in request.FILES:
#                # get picture from input form and put it in UserProfile model
#                profile.picture = request.FILES['picture']
#
#            profile.save()
#            registered = True#
#
#        else:
#            # print problems to the terminal
#            print(user_form.errors, profile_form.errors)
#    else:
#        # if not POST, empty form is displayed
#        user_form = UserForm()
#        profile_form = UserProfileForm()
#    
#    return render(request,
#                    'rango/register.html',
#                    context = {'user_form': user_form, # keys must be strings because they are used as template variables
#                                'profile_form': profile_form,
#                                'registered': registered})

#def user_login(request):
#    if request.method == 'POST':
#        # gather username and password provided by user from login form
#        username = request.POST.get('username')
#        password = request.POST.get('password')
#
#        # check whether username/password match a valid user account - User object is returned if it is (or None)
#        user = authenticate(username=username, password=password)
#
#        if user:
#            # account could have been disabled
#            if user.is_active:
#               login(request, user)
#                return redirect(reverse('rango:index'))
#            else:
#                return HttpResponse("Your Rango account is disabled.")
#        else:
#            print(f"Invalid login details: {username}, {password}")
#            return HttpResponse("Invalid login details supplied.")
#    else:
#        # GET - User visits /login/	-- django displays login form
#        # POST - User fills form & clicks "Login" -- django processes form data and logs user in
#        return render (request, 'rango/login.html')


# if user is NOT logged in, Django automatically redirects to LOGIN_URL
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

# login_required() decorator to ensure only those logged in can access view
#@login_required
#def user_logout(request):
#    logout(request)
#    # back to the homepage.
#    return redirect(reverse('rango:index'))






