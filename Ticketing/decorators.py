from django.http import HttpResponse
from django.shortcuts import redirect
from . import urls

#Create decorator to see if user is allowed in that page
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            #Initially, group have no value
            group = None
            #If the user is in a group, grab first group
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            #If his first group exists and is within allowed roles, continue function, allow login
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            #If he is not allowed to enter
            else:
                return HttpResponse('You are not authorised to view this page')
                
        return wrapper_func
    return decorator


def redirect_users(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None

        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'Employee':
            return view_func(request, *args, **kwargs)

        if group == 'Manager':
            return view_func(request, *args, **kwargs)
        
        if group == 'HR':
            return redirect('Training:HR_Ticket')
        
        if group =='HR Manager':
            return redirect('Training:HR_Ticket')

    return wrapper_function
