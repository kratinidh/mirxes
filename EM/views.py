from .decorators import allowed_users, redirect_users
from Profile.models import Profile, Departments

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import Group, User
from django.views.generic.edit import CreateView, UpdateView 
from django.contrib.auth.models import auth, Group, User
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, DeleteView
# Create your views here.

@login_required(login_url = 'login')
@redirect_users
@allowed_users(allowed_roles=['Employee', 'Manager', 'HR', 'HR Manager'])
def HR_EM(request):
    user_department= Departments.objects.get(name = 'HR')
    Profile_database = Profile.objects.exclude(department = user_department)

    context ={
        "profile_list": Profile_database
    }
    return render(request, 'EM/HuNet_HRem.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['HR Manager'])
def HRM_EM(request):
    Profile_database = Profile.objects.all()

    context ={
        "profile_list": Profile_database
    }
    return render(request, 'EM/HuNet_HRem.html', context)
    
class Create_Profile(CreateView):
    model = Profile
    fields = ['user', 'name', 'employee_ID', 'email', 'department', 'gender', 'address_1', 'address_2', 'marital_Status', 'date_Of_Passport_Expiry', 'citizenship_Status', 'date_Of_Hire', 'job_Title', 'employment_Type', 'first_Reporting_Manager', 'second_Reporting_Manager', 'division_Centre', 'qualification_Attained', 'skills', 'phone']
    success_url = reverse_lazy('EM:HR_EM')
    template_name = 'EM/HuNet_CreateProfile.html'

    def form_valid(self, form):
        print(form.cleaned_data)
        super(Create_Profile,self).form_valid(form)


class Update_Profile(UpdateView):
    model = Profile
    fields = ['user', 'name', 'employee_ID', 'email', 'department', 'gender', 'address_1', 'address_2', 'marital_Status', 'date_Of_Passport_Expiry', 'citizenship_Status', 'date_Of_Hire', 'job_Title', 'employment_Type', 'first_Reporting_Manager', 'second_Reporting_Manager', 'division_Centre', 'qualification_Attained', 'skills', 'phone']
    template_name = 'EM/HuNet_CreateProfile.html'
    success_url = reverse_lazy('EM:HR_EM')

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(Update_Profile,self).form_valid(form)

class Delete_Profile(DeleteView):
    template_name='EM/HuNet_DeleteProfile.html'
    success_url = reverse_lazy('EM:HR_EM')

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Profile, id=id)

class Profile_View(DetailView):
    template_name = 'EM/HuNet_DetailProfile.html'
    queryset = Profile.objects.all()

    def get_object(self):
        if self.request.user.is_authenticated:
            id = self.kwargs.get("pk")
            return get_object_or_404(Profile, id=id)
        else:
            return Profile.objects.none()

