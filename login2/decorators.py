from django.http import HttpResponse
from django.shortcuts import redirect
from . import urls


# First off, want to prevent people from accessing register and log in page when logged in

# A decorator is a function that takes in another function as a parameter and lets us add a little functionality before it is called, example for @unauthenticated_user, loginPage is view_func. It then run some checks and conditionals before returning as view_func. It doesnt get executed until wrapper function is executed

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user_homepage')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


# Create decorator to see if user is allowed in that page
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            # Initially, group have no value
            group = None
            # If the user is in a group, grab first group
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            # If his first group exists and is within allowed roles, continue function, allow login
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)

            # If he is not allowed to enter
            else:
                return HttpResponse('You are not authorised to view this page')

        return wrapper_func

    return decorator


# To check group of user and auto push them into respective dashboards
def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None

        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'Employee':
            return view_func(request, *args, **kwargs)

        elif group == 'Manager':
            return redirect('manager_homepage')

        elif group == 'HR':
            return redirect('hr_homepage')

        elif group == 'HR manager':
            return redirect('hrmanager_homepage')

    return wrapper_function
