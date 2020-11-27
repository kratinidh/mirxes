from .forms import GoalsForm, DepartmentGoalsForm, CompetenciesForm, CreateGoalsForm, CreateCompetenciesForm, CreateKPIsForm, UpdateKPIsForm ,CreateDepartmentalGoalsForm, CreateDepartmentalCompetenciesForm, UpdatePOSTKPIsForm, UploadGoalsEvidence
from .models import Goals, Competencies, goal_category, Departmental_Goals, KPI, competency_category, goal_comment, competency_comment, Departmental_Competencies
from .decorators import allowed_users, redirect_users
from Profile.models import Profile, Departments
from Appraisals.models import Appraisal, User_Appraisal_List, Overall_Appraisal

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.views.generic.edit import CreateView,  UpdateView
from django.views.generic import DetailView, DeleteView
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.contrib import messages 

from bootstrap_modal_forms.generic import BSModalCreateView

class ExtraContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(ExtraContextMixin, self).get_context_data(**kwargs)
        context.update(self.extra())
        return context
    
    def extra(self):
        return dict()

@login_required(login_url = 'login')
@redirect_users
@allowed_users(allowed_roles=['Employee'])
def User_GnC(request):
    #returns all goals set by login user

    #Get user's profile and retrieve all his user goals
    goals_database = request.user.profile.goals_set.all()

    #Get user's profile and retrieve all his competencies goals
    competencies_database= request.user.profile.competencies_set.all()

    #Get all goal categories in database
    goal_category_database = goal_category.objects.all()

    #1.Get profile of logged in user
    userprofile = Profile.objects.get(user=request.user)
    #2.Get departmental goals of user manager
    departmental_goals_database = Departmental_Goals.objects.filter(manager=userprofile.first_Reporting_Manager)

    context ={
        "departmental_goals_list":departmental_goals_database,
        "goals_list":goals_database,
        "competencies_list":competencies_database,
        "goal_category": goal_category_database
    }

    return render(request,'GnC/HuNet_GnC.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['Manager'])
def Manager_GnC(request):
    #Get user's profile and retrieve all his user goals
    goals_database = request.user.profile.goals_set.all()

    #Get user's profile and retrieve all his competencies goals
    competencies_database= request.user.profile.competencies_set.all()

    #1.Get profile of logged in user
    userprofile_M = Profile.objects.get(user=request.user).first_Reporting_Manager
    #2.Get manager departmental goals
    manager_departmental_goals_database = Departmental_Goals.objects.filter(manager = userprofile_M)

    #1.Get profile of logged in user
    userprofile_M = Profile.objects.get(user = request.user).first_Reporting_Manager
    #2.Get manager departmental goals
    manager_departmental_competencies_database = Departmental_Competencies.objects.filter(manager = userprofile_M)

    #1.Get profile of logged in manager
    userprofile = Profile.objects.get(user=request.user)
    #2.Get all his subordinates
    surbordinates = Profile.objects.filter(first_Reporting_Manager = userprofile)
    #competencies_counter = department_database.competencies_set.all().count
    #goals_counter = department_database.goals_set.all().count

    context ={
        "goals_list":goals_database,        
        "competencies_list":competencies_database,
        "departmental_goals_list":manager_departmental_goals_database,

        "departmental_competencies_list":manager_departmental_competencies_database,

        "department_detailed_view":surbordinates,

        #"goals_count": goals_counter,
        #"competencies_count": competencies_counter
    }
    return render(request, 'GnC/HuNetM_GnC.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['HR'])
def HR_GnC(request):
    #1.Get profile of logged in user
    userprofile = Profile.objects.get(user=request.user)

    #2.Get departmental goals of user manager
    departmental_goals_database = Departmental_Goals.objects.filter(manager=userprofile.first_Reporting_Manager)
    
    #User - Personal Goals:
    goals_database = request.user.profile.goals_set.all()

    #User - Competencies:
    competencies_database= request.user.profile.competencies_set.all()

    #Department List:
    company_department_database = Departments.objects.all()

    #Employee List:
    company_user_database = Profile.objects.exclude(department = userprofile.department ).order_by('name')

    context = {
        "Personal_departmental_goals_list": departmental_goals_database,
        "Personal_goals_list": goals_database,
        "Personal_competencies_list" : competencies_database,
        "Company_department_list":company_department_database,  
        "Company_user_list": company_user_database
    }

    return render(request, 'GnC/HuNetRoot_GnC.html', context)


#@login_required(login_url = 'login')
#@allowed_users(allowed_roles=['Employee', 'Manager', #'HR', 'HR manager'])
#def Create_Departmental_Goals(request):
#    form = DepartmentGoalsForm()
#    if (request.method == 'POST'):
#        form = DepartmentGoalsForm(request.POST)
#        if form.is_valid:
#           form.save()
#           return redirect("../")
#    
#    context = {'form':form}
#    return render(request, 'GnC/HuNetM_CreateGoals.#html', context)

#Form class
#CreateView
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['Employee', 'Manager', 'HR', 'HR manager']), name='dispatch')
class Create_Goals(BSModalCreateView): #class Create_Goals(CreateView): 
    success_message = 'Success: Goal was created.'
    form_class = CreateGoalsForm
    success_url = reverse_lazy('user_homepage')
    template_name = 'GnC/HuNet_CreateGoals.html'

    def clean(self, *args, **kwargs):
        cleaned_data = super(Create_Goals, self).clean()
        id = self.kwargs.get("pk")
        user_appraisal_list = User_Appraisal_List.objects.get(id=id)
        for goal in user_appraisal_list.goals_set.all():
            sum += int(goal.weightage)

        field_1 = cleaned_data.get('weightage')

        if ((sum + int(field_1)>=101) or int(field_1)!=1):
            #self.add_error(None, ValidationError("Weightage exceeded 100%"))         
            raise ValidationError({'weightage': ('Maximum weightage of 100 in this appraisal exceeded')})
        
        return cleaned_data

    def form_valid(self, form):
        id = self.kwargs.get("pk")
        user_appraisal_list = User_Appraisal_List.objects.get(id=id)

        form.instance.appraisal = user_appraisal_list
        form.instance.employee = self.request.user.profile
        form.instance.status = 'Employee'

        print(form.cleaned_data)
        return super(Create_Goals, self).form_valid(form)


#Form done
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['Employee', 'Manager', 'HR', 'HR manager']), name='dispatch')
class Create_Competencies(CreateView):
    form_class = CreateCompetenciesForm
    success_url = reverse_lazy('user_homepage')
    template_name = 'GnC/HuNet_CreateCompetencies.html'

    def form_valid(self, form):
        id = self.kwargs.get("pk")
        user_appraisal_list = User_Appraisal_List.objects.get(id=id)

        form.instance.appraisal = user_appraisal_list
        form.instance.employee = self.request.user.profile

        print(form.cleaned_data)
        return super(Create_Competencies, self).form_valid(form)

#Form done
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['Employee', 'Manager', 'HR', 'HR manager']), name='dispatch')
class Create_KPI(CreateView):
    form_class = CreateKPIsForm
    success_url = reverse_lazy('user_homepage')
    template_name = 'GnC/HuNet_CreateKPI.html'

    def form_valid(self, form):
        id = self.kwargs.get("pk")
        form.instance.goal = Goals.objects.get(id=id)
        form.instance.progress = 'Not Started'
        print(form.cleaned_data)
        return super(Create_KPI, self).form_valid(form)

#Form done
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['Employee', 'Manager', 'HR', 'HR manager']), name='dispatch')
class Create_Departmental_Goals(CreateView):
    form_class = CreateDepartmentalGoalsForm
    success_url = reverse_lazy('user_homepage')
    template_name = 'GnC/HuNet_CreateDepartmentalGoals.html'

    def form_valid(self, form):
        id = self.kwargs.get("pk")
        form.instance.appraisal = Overall_Appraisal.objects.get(id=id)
        #To automatically pass user profile into 'manager' field
        form.instance.manager = self.request.user.profile 
        form.instance.department = self.request.user.profile.department
        print(form.cleaned_data)
        return super(Create_Departmental_Goals, self).form_valid(form)

#Form done
@method_decorator(login_required(login_url='login'), name='dispatch')
class Create_Departmental_Competencies(CreateView):
    form_class = CreateDepartmentalCompetenciesForm
    template_name = 'GnC/HuNet_CreateCompetencies.html'
    success_url = reverse_lazy('user_homepage')

    def form_valid(self, form):
        id = self.kwargs.get("pk")
        form.instance.appraisal = Overall_Appraisal.objects.get(id=id)
        form.instance.manager = self.request.user.profile
        form.instance.department = self.request.user.profile.department
        print(form.cleaned_data)
        return super(Create_Departmental_Competencies, self).form_valid(form) 

@method_decorator(login_required(login_url='login'), name='dispatch')
class Create_Goals_Comments(CreateView):
    model = goal_comment
    fields = ['comments']
    template_name = 'GnC/Hunet_CreateGoals.html'
    success_url = reverse_lazy('user_homepage')

    def form_valid(self, form):
        form.instance.created_by = self.request.user.profile
        id=self.kwargs.get("pk")
        form.instance.goal = Goals.objects.get(id=id)
        print(form.cleaned_data)
        return super(Create_Goals_Comments, self).form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class Create_Competencies_Comments(CreateView):
    model = competency_comment
    fields = ['comments']
    template_name = 'GnC/HuNet_CreateCompetencies.html'
    success_url = reverse_lazy('user_homepage')

    def form_valid(self, form):
        form.instance.created_by = self.request.user.profile
        id = self.kwargs.get("pk")
        form.instance.competency = Competencies.objects.get(id = id)
        print(form.cleaned_data)
        super(Create_Competencies_Comments, self).form_valid(form)

#DetailView
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['Employee', 'Manager', 'HR', 'HR manager']), name='dispatch')
class Departmental_Goals_View(DetailView):
    template_name = 'GnC/HuNet_DetailDepartmentalGoals.html'
    queryset = Departmental_Goals.objects.all()

    def get_object(self):
        if self.request.user.is_authenticated:
            id = self.kwargs.get("pk")
            return Departmental_Goals.objects.get(id = id)
        else:
            return Departmental_Goals.objects.none()

@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['Employee', 'Manager', 'HR', 'HR manager']), name='dispatch')
class Goals_View(DetailView):
    template_name = 'GnC/HuNet_DetailGoals.html'
    queryset = Goals.objects.all()

    def get_object(self):
        if self.request.user.is_authenticated:
            id = self.kwargs.get("pk")
            return Goals.objects.get(id=id)
        
        else:
            return queryset.none()

@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['Employee', 'Manager', 'HR', 'HR manager']), name = 'dispatch')
class Competencies_View(DetailView):
    template_name = 'GnC/HuNet_DetailCompetencies.html'
    queryset = Competencies.objects.all()

    def get_object(self):
        if self.request.user.is_authenticated:
            id=self.kwargs.get("pk")
            return Competencies.objects.get(id=id)
        else:
            return Competencies.objects.none()

@method_decorator(login_required(login_url='login'), name='dispatch')
class HRDepartment_view(DetailView):
    template_name='GnC/HuNetHR_DetailDepartment.html'
    queryset = Departments.objects.all()

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Departments, id=id)

@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['Employee', 'Manager', 'HR', 'HR manager']), name='dispatch')
class Department_View(ExtraContextMixin, DetailView):
    template_name = 'GnC/HuNet_DetailDepartment.html'
    queryset = Profile.objects.all()

    def extra(self):
        extra = Goals.objects.all()
        return dict(extra = extra)


#DeleteView
@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['Employee', 'Manager', 'HR', 'HR manager']), name='dispatch')
class Goals_Delete(DeleteView):
    model = Goals
    template_name = 'GnC/HuNet_DeleteGoals.html'
    success_url = reverse_lazy('user_homepage')

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Goals, id = id)

    def get_success_url(self):
        return reverse('user_homepage')

@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['Employee', 'Manager', 'HR', 'HR manager']), name='dispatch')
class Competencies_Delete(DeleteView):
    model = Competencies
    template_name = 'GnC/HuNet_DeleteCompetencies.html'

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Competencies, id = id)

    def get_success_url(self):
        return reverse('user_homepage')

@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_users(allowed_roles=['Employee', 'Manager', 'HR', 'HR manager']), name='dispatch')
class Departmental_Goals_Delete(DeleteView):
    template_name = 'GnC/HuNet_DeleteGoals.html'
    success_url = reverse_lazy('user_homepage')

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Departmental_Goals, id = id)

class Departmental_Competencies_Delete(DeleteView):
    template_name = 'GnC/HuNet_DeleteCompetencies.html'
    success_url = reverse_lazy('user_homepage')

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Departmental_Competencies, id = id)

@method_decorator(login_required(login_url='login'), name='dispatch')
class KPI_Delete(DeleteView):
    template_name = 'GnC/HuNet_DeleteK.html'
    success_url = reverse_lazy ('user_homepage')

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(KPI, id=id)


#UpdateView
#Form done
#Update goals (User view)
@method_decorator(login_required(login_url='login'), name='dispatch')
class Update_Goals_User(UpdateView):
    model = Goals
    form_class = CreateGoalsForm
    template_name = 'GnC/HuNet_CreateGoals.html'
    success_url = reverse_lazy('user_homepage')

    def form_valid(self, form):
        form.instance.status = 'Manager'
        print(form.cleaned_data)
        return super(Update_Goals_User, self).form_valid(form)

#Form done
#Update departmental goal
@method_decorator(login_required(login_url='login'), name='dispatch')
class Update_Departmental_Goals(UpdateView):
    model = Departmental_Goals
    form_class = CreateDepartmentalGoalsForm
    template_name = 'GnC/HuNet_CreateDepartmentalGoals.html'
    success_url = reverse_lazy('user_homepage')

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(Update_Departmental_Goals, self).form_valid(form)

#Form done
@method_decorator(login_required(login_url='login'), name='dispatch')
class Update_Departmental_Competencies(UpdateView):
    model = Departmental_Competencies
    form_class = CreateDepartmentalCompetenciesForm
    template_name = 'GnC/HuNet_CreateCompetencies.html'
    success_url = reverse_lazy('user_homepage')

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(Update_Departmental_Competencies, self).form_valid(form)

#Form done
#Update competencies (user view)
@method_decorator(login_required(login_url='login'), name='dispatch')
class Update_Competencies_User(UpdateView):
    model = Competencies
    form_class = CreateCompetenciesForm
    template_name = 'GnC/GnCUpdateCompetencies.html'
    success_url = reverse_lazy('user_homepage')

    def form_valid(self, form):
        form.instance.status = 'Manager'
        print(form.cleaned_data)
        return super(Update_Competencies_User, self).form_valid(form)

#Form done
#Update KPI (user view)
@method_decorator(login_required(login_url='login'), name='dispatch')
class Update_KPI(UpdateView):
    model = KPI
    form_class = UpdateKPIsForm
    template_name = 'GnC/HuNet_UpdateKPI.html'
    success_url = reverse_lazy('user_homepage')

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(Update_KPI, self).form_valid(form)

#Form done
@method_decorator(login_required(login_url='login'), name='dispatch')
class Update_KPI_POST(UpdateView):
    model = KPI
    form_class = UpdatePOSTKPIsForm
    template_name = 'GnC/HuNet_CreateKPI.html'
    success_url = reverse_lazy('user_homepage')

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(Update_KPI_POST, self).form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class Update_KPI_POST1(UpdateView):
    model = KPI
    fields=[]
    template_name = 'GnC/UpdateKPIStatus1.html'
    success_url = reverse_lazy('user_homepage')

    def form_valid(self, form):
        form.instance.progress = 'Completed'
        print(form.cleaned_data)
        return super(Update_KPI_POST1, self).form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class Update_KPI_POST2(UpdateView):
    model = KPI
    fields=[]
    template_name = 'GnC/UpdateKPIStatus2.html'
    success_url = reverse_lazy('user_homepage')

    def form_valid(self, form):
        form.instance.progress = 'Working'
        print(form.cleaned_data)
        return super(Update_KPI_POST2, self).form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class Update_Departments(UpdateView):
    model = Departments
    fields = ['manager']
    template_name = 'GnC/HuNet_CreateGoals.html'
    success_url = reverse_lazy('user_homepage')

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(Update_Departments, self).form_valid(form)

@login_required(login_url='login')
def createGoals(request, *args, **kwargs):
    id = kwargs.get('pk')
    user_appraisal_list = User_Appraisal_List.objects.get(id=id)
    appraisal_list = user_appraisal_list.goals_set.all()
    sum=0
    form_class = CreateGoalsForm
    form = form_class
    
    for goal in appraisal_list:
        sum += int(goal.weightage)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.appraisal = user_appraisal_list
            goal.employee = request.user.profile
            if(goal.weightage + sum > 100):
                messages.warning(request, 'Total Goal weightage exceeded 100%')
                return HttpResponseRedirect(reverse('GnC:Create_User_Goals', args=(id,)))
            goal.save()
            return HttpResponseRedirect(reverse('user_homepage')) 
                
    context={'formset': form}
    return render(request, 'GnC/GnCCreateGoals.html', context)

@login_required(login_url='login')
def updateGoals(request, *args, **kwargs):
    id = kwargs.get('pk')
    user_appraisal_list = User_Appraisal_List.objects.get(id=id)
    appraisal_list = user_appraisal_list.goals_set.all()
    
    _id = kwargs.get('mk')
    obj = get_object_or_404(Goals, id=_id)

    sum=0
    form_class = CreateGoalsForm
    form = form_class
    
    for goal in appraisal_list:
        sum += int(goal.weightage)
    sum -= int(obj.weightage)

    form = CreateGoalsForm(request.POST or None, instance=obj)
    if form.is_valid():
        goal = form.save(commit=False)
        if(goal.weightage + sum > 100):
            messages.warning(request, 'Total Goal weightage exceeded 100%')
            return HttpResponseRedirect(reverse('GnC:Update_User_Goals', args=(id, _id,)))
        goal.save()
        return HttpResponseRedirect(reverse('user_homepage')) 
                
    context={'formset': form}
    return render(request, 'GnC/GnCUpdateGoals.html', context)

@login_required(login_url='login')
def GoalsImage(request, *args, **kwargs):
    id = kwargs.get('pk')
    goal = Goals.objects.get(id=id)

    context={
        'goals': goal
    }
    return render(request, 'GnC/GoalsImageView.html', context)

@login_required(login_url='login')
def GoalsImageUpload(request, *args, **kwargs):
    id = kwargs.get('pk')
    goal = Goals.objects.get(id=id)
    form = UploadGoalsEvidence(request.POST, request.FILES, instance = goal)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user_homepage')) 

    context={
        'form': form
    }
    return render(request, 'GnC/GoalsImageUpload.html', context)
