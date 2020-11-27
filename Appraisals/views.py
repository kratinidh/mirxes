import csv

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from Profile.models import Profile, Departments
from .models import Appraisal_Category, Overall_Appraisal, Rating_Scale, User_Appraisal_List, Appraisal, peerAppraisal, peerAppraisalQuestion
from GnC.models import Goals, Competencies
from Trainings.models import Skills, Career_Discussion
#from .forms import CreateAppraisalForm, GoalsFormset, CompetenciesFormset
from .decorators import unauthenticated_user, allowed_users, redirect_users
from .forms import AppGoalsForm, AppCompetenciesForm, peerAppraisalForm, MAppCompetenciesForm, MAppGoalsForm, BAppGoalsForm, BAppCompetenciesForm, CreateAppraisalCategoryForm, CreateRatingScaleForm, UpdateOverallAppraisalForm, AppSkillsForm, MAppSkillsForm, BAppSkillsForm, TryingOutForm, CreateOverallAppraisalForm_Stage1, CreateOverallAppraisalForm_Stage3, CreateOverallAppraisalForm_Stage4, MidAppGoalsForm, MidAppGoalsForm_M, BAppForm, UpdateUserAppRatingForm, UpdateManagerAppRatingForm, UpdateBoardAppRatingForm, AppraisalRejectionForm, GoalsSettingRejectionForm, MidYearRejectionForm ,CreateCareerDiscussionForm, CreateCareerDiscussionForm2, CreatePeerAppraisalForm,UpdatePeerAppraisalForm
from django.contrib import messages

from shapeshifter.views import MultiFormView, MultiModelFormView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.views.generic.edit import CreateView,  UpdateView
from django.views.generic import DetailView, DeleteView
from django.utils.decorators import method_decorator
from django.forms.models import modelformset_factory, inlineformset_factory
from bootstrap_modal_forms.generic import BSModalDeleteView

def APPRAISAL_LAUNCHING_EMAIL(overall_appraisal): 
    email_string = "Dear user, \n\nThe Performance Appraisal Exercise has started! \n\nPlease see the deadlines for the various stages below \n\t 1.Goals Setting Exercise: " + str(overall_appraisal.goals_setting_end_date) + "\n\t 2.Mid-Year Review:" +  str(overall_appraisal.mid_year_end_date) + "\n\t 3.Year-End Review: " + str(overall_appraisal.appraisal_end_date) + "\n\t 4.Reports: " + str(overall_appraisal.reports_end_date) + "\n\t 5.Calibration: " +str(overall_appraisal.calibration_end_date) + "\n\nWhat's next? \nLogin to your account to add your Goals, Core Values Competencies and Skills. \n\nPlease do not hesitate to contact the HR Department if you have any questions. \nThank you."
    return email_string

def MID_YEAR_REVIEW_EMAIL(dateline): 
    email_string = "Dear user, \n\nThe Mid-Year Review has started!\nPlease remember to complete your Mid-Year review form by " + dateline + "\n\nPlease do not hesitate to contact the HR Department if you have any questions.\nThank you."
    return email_string

def YEAR_END_REVIEW_EMAIL(dateline): 
    email_string = "Dear user, \n\nThe Year-End Review has started!\nPlease remember to complete your Year-End rating form by " + dateline + "\n\nPlease do not hesitate to contact the HR Department if you have any questions.\nThank you."
    return email_string

def GRADING_SYSTEM(x):
    if x>= 5:
        return 'Grade: Far Exceed Expectations'
    
    elif x>= 4:
        return 'Grade: Exceeds Expectations'

    elif x>= 3:
        return 'Grade: Meets Expectations'

    elif x>= 2:
        return 'Grade: Needs Improvement'

    elif x>= 1:
        return 'Grade: Major Improvement needed'

    else:
        return 'Ungraded'

def FINAL_GRADE(selfappraisal, overallappraisal):
    #Goals
    sum = 0
    weightage_count=0
    totalsum = 0
    for goal in selfappraisal.goals_set.all():
        weightage_count+=goal.weightage
    for goal in selfappraisal.goals_set.all():
        sum+=goal.user_rating * goal.weightage / weightage_count
    totalsum += sum * overallappraisal.goal_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)

    sum = 0
    weightage_count = 0
    for competency in selfappraisal.competencies_set.all():
        weightage_count+=competency.weightage
    for competency in selfappraisal.competencies_set.all():
        sum+=competency.user_rating * competency.weightage / weightage_count
    totalsum += sum * overallappraisal.competency_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)

    sum = 0
    weightage_count = 0
    for skill in selfappraisal.skills_set.all():
        weightage_count+=skill.weightage
    for skill in selfappraisal.skills_set.all():
        sum+=skill.user_rating * skill.weightage / weightage_count
    totalsum += sum * overallappraisal.skill_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)

    totalavg = round(totalsum,1)

    return totalavg
    #return GRADING_SYSTEM(totalavg)

def M_FINAL_GRADE(selfappraisal, overallappraisal):
    #Goals
    sum = 0
    weightage_count=0
    totalsum = 0
    for goal in selfappraisal.goals_set.all():
        weightage_count+=goal.weightage
    for goal in selfappraisal.goals_set.all():
        sum+=goal.manager_rating * goal.weightage / weightage_count
    totalsum += sum * overallappraisal.goal_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)

    sum = 0
    weightage_count = 0
    for competency in selfappraisal.competencies_set.all():
        weightage_count+=competency.weightage
    for competency in selfappraisal.competencies_set.all():
        sum+=competency.manager_rating * competency.weightage / weightage_count
    totalsum += sum * overallappraisal.competency_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)

    sum = 0
    weightage_count = 0
    for skill in selfappraisal.skills_set.all():
        weightage_count+=skill.weightage
    for skill in selfappraisal.skills_set.all():
        sum+=skill.manager_rating * skill.weightage / weightage_count
    totalsum += sum * overallappraisal.skill_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)

    totalavg = round(totalsum,1)

    return totalavg
    #return GRADING_SYSTEM(totalavg)

def B_FINAL_GRADE(selfappraisal, overallappraisal):
    #Goals
    sum = 0
    weightage_count=0
    totalsum = 0
    for goal in selfappraisal.goals_set.all():
        weightage_count+=goal.weightage
    for goal in selfappraisal.goals_set.all():
        sum+=goal.board_rating * goal.weightage / weightage_count
    totalsum += sum * overallappraisal.goal_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)

    sum = 0
    weightage_count = 0
    for competency in selfappraisal.competencies_set.all():
        weightage_count+=competency.weightage
    for competency in selfappraisal.competencies_set.all():
        sum+=competency.board_rating * competency.weightage / weightage_count
    totalsum += sum * overallappraisal.competency_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)

    sum = 0
    weightage_count = 0
    for skill in selfappraisal.skills_set.all():
        weightage_count+=skill.weightage
    for skill in selfappraisal.skills_set.all():
        sum+=skill.board_rating * skill.weightage / weightage_count
    totalsum += sum * overallappraisal.skill_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)

    totalavg = round(totalsum,1)

    return totalavg
   #return GRADING_SYSTEM(totalavg)

#Done
@method_decorator(login_required(login_url='login'), name='dispatch')
class Create_Appraisal_Category(CreateView):
    form_class = CreateAppraisalCategoryForm
    success_url = reverse_lazy('Appraisals:User_Appraisals')
    template_name = 'Appraisals/HuNet_CreateAppCat.html'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(Create_Appraisal_Category, self).form_valid(form)

#Done
@method_decorator(login_required(login_url='login'), name='dispatch')
class Create_Rating_Scale(CreateView):
    form_class = CreateRatingScaleForm
    success_url = reverse_lazy('Appraisals:User_Appraisals')
    template_name = 'Appraisals/HuNet_CreateRatingScale.html'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(Create_Rating_Scale, self).form_valid(form)

#useless fx
@method_decorator(login_required(login_url='login'), name='dispatch')
class Create_User_Appraisal_List(CreateView):
    model = User_Appraisal_List
    fields = ['employee','manager']
    success_url = reverse_lazy('Appraisals:User_Appraisals')
    template_name = 'Appraisals/HuNet_Create.html'

    def form_valid(self, form):
        id = self.kwargs.get("pk")
        overall_appraisal = Overall_Appraisal.objects.get(id=id)

        form.instance.overall_appraisal = overall_appraisal
        form.instance.start_date = overall_appraisal.start_date
        form.instance.end_date = overall_appraisal.calibration_end_date
        form.instance.appraisal_name = overall_appraisal.name
        form.instance.appraisal_category = overall_appraisal.appraisal_category
 
        print(form.cleaned_data)
        return super(Create_User_Appraisal_List, self).form_valid(form)

#------------UpdateView----------#
#Done
@method_decorator(login_required(login_url='login'), name='dispatch')
class Update_Appraisal_Category(UpdateView):
    form_class = CreateAppraisalCategoryForm
    success_url = reverse_lazy('user_homepage')
    template_name = 'Appraisals/HuNet_CreateAppCat.html'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(Update_Appraisal_Category, self).form_valid(form)


#Done
@method_decorator(login_required(login_url='login'), name='dispatch')
class Update_Rating_Scale(UpdateView):
    model = Rating_Scale
    form_class = CreateRatingScaleForm
    success_url = reverse_lazy('Appraisals:User_Appraisals')
    template_name = 'Appraisals/HuNet_CreateRatingScale.html'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(Update_Rating_Scale, self).form_valid(form)
        
@method_decorator(login_required(login_url='login'), name='dispatch')
class Update_User_Appraisal_List(UpdateView):
    model = User_Appraisal_List
    fields = ['employee', 'manager', 'overall_appraisal']
    success_url = reverse_lazy('Appraisals:User_Appraisals')
    template_name = 'Appraisals/HuNet_UpdateUAL.html'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(Update_User_Appraisal_List, self).form_valid(form)
#class Update_peerAppraisal(UpdateView):
#    model = Appraisal
#    fields = ['employee_list', 'title']
#    success_url = reverse_lazy('Appraisals:User_Appraisals')
#    template_name = 'Appraisals/HuNet_Create.html'

#    def form_valid(self, form):
#        print(form.cleaned_data)
#        return super(Update_peerAppraisal, self).form_valid(form)

#-------------------UpdateView---------------------#

@method_decorator(login_required(login_url='login'), name='dispatch')
class Delete_Appraisal_Category(DeleteView):
    model = Appraisal_Category
    template_name = 'Appraisals/Delete_AppCat.html'
    success_url = reverse_lazy('Appraisals:User_Appraisals')

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Appraisal_Category, id=id)

@method_decorator(login_required(login_url='login'), name='dispatch')
class Delete_Overall_Appraisal(BSModalDeleteView):
    model = Overall_Appraisal
    template_name = 'Appraisals/Delete_OverallApp.html'
    success_url = reverse_lazy('user_homepage')
    success_message = ''

@method_decorator(login_required(login_url='login'), name='dispatch')
class Delete_Rating_Scale(DeleteView):
    model = Rating_Scale
    template_name = 'Appraisals/Delete_RatingScale.html'
    success_url = reverse_lazy('Appraisals:User_Appraisals')

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Rating_Scale, id=id)

@method_decorator(login_required(login_url='login'), name='dispatch')
class Delete_User_Appraisal_List(DeleteView):
    model = User_Appraisal_List
    template_name = 'Appraisals/Delete_UAL.html'
    success_url = reverse_lazy('Appraisals:User_Appraisals')

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(User_Appraisal_List, id=id)

#Useless fx
@method_decorator(login_required(login_url='login'), name='dispatch')
class Delete_Appraisal(DeleteView):
    model = Appraisal
    template_name = 'Appraisals/HuNet_Delete.html'
    success_url = reverse_lazy('Appraisals:User_Appraisals')

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Appraisal, id=id)

@method_decorator(login_required(login_url='login'), name='dispatch')
class Delete_peerAppraisal(DeleteView):
    model = peerAppraisal
    template_name = 'Appraisals/Delete_peerApp.html'
    success_url = reverse_lazy('Appraisals:User_Appraisals')

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(peerAppraisal, id=id)

#------------------DetailView--------------------#

@method_decorator(login_required(login_url='login'), name='dispatch')
class Detail_Overall_Appraisal(DetailView):
    model = Overall_Appraisal
    template_name = 'Appraisals/HuNet_DetailOverallApp.html'
    success_url = reverse_lazy('Appraisals:User_Appraisals')

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Overall_Appraisal, id=id)
 
@method_decorator(login_required(login_url='login'), name='dispatch')
class Detail_User_Appraisal_List(DetailView):
    model = User_Appraisal_List
    template_name = 'Appraisals/HuNet_DetailUserAppraisal.html'
    success_url = reverse_lazy('Appraisals:User_Appraisals')

    def get_object(self):
        id = self.kwargs.get("mk")
        return get_object_or_404(User_Appraisal_List, id=id)

@method_decorator(login_required(login_url='login'), name='dispatch')
class Detail_HRUser_Appraisal_List(DetailView):
    model = User_Appraisal_List
    template_name = 'Appraisals/HuNet_HRDetailUserAppraisal.html'
    success_url = reverse_lazy('Appraisals:User_Appraisals')

    def get_object(self):
        id = self.kwargs.get("mk")
        return get_object_or_404(User_Appraisal_List, id=id)

#####################################################

#I think useless
@login_required(login_url='login')
def UpdateAppraisal(request, *args, **kwargs):
    id = kwargs.get('mk')
    selfappraisal = get_object_or_404(User_Appraisal_List, id=id)

    GoalsFormset=modelformset_factory(Goals, form = AppGoalsForm, extra = 0)
    queryset1=Goals.objects.filter(appraisal = selfappraisal, employee = selfappraisal.employee)

        
  #  CompetenciesFormset=modelformset_factory(Competencies, form = AppCompetenciesForm, extra = 0)
  #  queryset2=Competencies.objects.filter(appraisal = selfappraisal, employee = selfappraisal.employee)
    
    if request.method == 'POST':
        formset = GoalsFormset(request.POST or None, queryset = queryset1)
       # formset2= CompetenciesFormset(request.POST or None, queryset = queryset2)
        if formset.is_valid():
           # competencies = formset2.save(commit=False)
            goals = formset.save(commit=False)
          #  for competency in competencies:
          #      competency.save()
            for goal in goals:
                goal.save()  
            return redirect('../../../../userhome')  
        
    else:
        formset = GoalsFormset(queryset = queryset1)
       # formset2 = CompetenciesFormset(queryset = queryset2)


    context ={
        "goals_formset": formset,
      #  "competencies_formset": formset2
    }
    return render(request, 'Appraisals/HuNet_Update.html', context)

@method_decorator(login_required(login_url='login'), name='dispatch')
class EtM_User_Appraisal_List(UpdateView):
    model = User_Appraisal_List
    fields = []
    success_url = reverse_lazy('user_homepage')
    template_name = 'Appraisals/Update_EtM_UAL.html'

    def form_valid(self, form):
        form.instance.status = 'Manager'
        print(form.cleaned_data)
        return super(EtM_User_Appraisal_List, self).form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class MtE_User_Appraisal_List(UpdateView):
    model = User_Appraisal_List
    form_class = GoalsSettingRejectionForm
    success_url = reverse_lazy('user_homepage')
    template_name = 'Appraisals/Update_MtE_UAL.html'

    def form_valid(self, form):
        form.instance.status = 'Employee'
        print(form.cleaned_data)
        return super(MtE_User_Appraisal_List, self).form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class MtS1BE_User_Appraisal_List(UpdateView):
    model = User_Appraisal_List
    fields = []
    success_url = reverse_lazy('user_homepage')
    template_name = 'Appraisals/Update_MtS1BE_UAL.html'

    def form_valid(self, form):
        form.instance.status = 'S1BEmployee'
        print(form.cleaned_data)
        return super(MtS1BE_User_Appraisal_List, self).form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class S1BEtS1BM_User_Appraisal_List(UpdateView):
    model = User_Appraisal_List
    fields = []
    success_url = reverse_lazy('user_homepage')
    template_name = 'Appraisals/Update_S1BEtS1BM_UAL.html'

    def form_valid(self, form):
        form.instance.status = 'S1BManager'
        print(form.cleaned_data)
        return super(S1BEtS1BM_User_Appraisal_List, self).form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class S1BMtS1BR_User_Appraisal_List(UpdateView):
    model = User_Appraisal_List
    form_class = MidYearRejectionForm
    success_url = reverse_lazy('user_homepage')
    template_name = 'Appraisals/Update_S1BMtS1BR_UAL.html'

    def form_valid(self, form):
        form.instance.status = 'S1BReview'
        print(form.cleaned_data)
        return super(S1BMtS1BR_User_Appraisal_List, self).form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class S1BRtS1BM_User_Appraisal_List(UpdateView):
    model = User_Appraisal_List
    fields = []
    success_url = reverse_lazy('user_homepage')
    template_name = 'Appraisals/Update_S1BRtS1BM_UAL.html'

    def form_valid(self, form):
        form.instance.status = 'S1BManager'
        print(form.cleaned_data)
        return super(S1BRtS1BM_User_Appraisal_List, self).form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class S1BMtS2E_User_Appraisal_List(UpdateView):
    model = User_Appraisal_List
    fields = []
    success_url = reverse_lazy('user_homepage')
    template_name = 'Appraisals/Update_S1BMtS2E_UAL.html'

    def form_valid(self, form):
        form.instance.status = 'S2Employee'
        print(form.cleaned_data)
        return super(S1BMtS2E_User_Appraisal_List, self).form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class S2EtS2M_User_Appraisal_List(UpdateView):
    model = User_Appraisal_List
    fields = []
    success_url = reverse_lazy('user_homepage')
    template_name = 'Appraisals/Update_S2EtS2M_UAL.html'

    def form_valid(self, form):
        form.instance.status = 'S2Manager'
        print(form.cleaned_data)
        return super(S2EtS2M_User_Appraisal_List, self).form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class S2MtApp_User_Appraisal_List(UpdateView):
    model = User_Appraisal_List
    fields = []
    success_url = reverse_lazy('user_homepage')
    template_name = 'Appraisals/Update_S2MtApp_UAL.html'

    def form_valid(self, form):
        form.instance.status = 'Approved'
        print(form.cleaned_data)
        return super(S2MtApp_User_Appraisal_List, self).form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class ApptS2M_User_Appraisal_List(UpdateView):
    model = User_Appraisal_List
    form_class = AppraisalRejectionForm
    success_url = reverse_lazy('user_homepage')
    template_name = 'Appraisals/Update_ApptS2M_UAL.html'

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(User_Appraisal_List, id=id)

    def form_valid(self, form):
        form.instance.status = 'S2Manager'
        form.instance.completion = 'Review'
        print(form.cleaned_data)
        return super(ApptS2M_User_Appraisal_List, self).form_valid(form)

@method_decorator(login_required(login_url='login'), name='dispatch')
class S2MtAppR_User_Appraisal_List(UpdateView):
    model = User_Appraisal_List
    fields = []
    success_url = reverse_lazy('user_homepage')
    template_name = 'Appraisals/Update_S2MtAppR_UAL.html'

    def form_valid(self, form):
        form.instance.status = 'Approved'
        form.instance.completion = 'ReviewCompleted'
        print(form.cleaned_data)
        return super(S2MtAppR_User_Appraisal_List, self).form_valid(form)

@login_required(login_url='login')
def UpdateMidAppraisalG(request, *args, **kwargs):
    id = kwargs.get('pk')
    selfappraisal = get_object_or_404(User_Appraisal_List, id=id)

    GoalsFormset=modelformset_factory(Goals, form = MidAppGoalsForm, extra = 0)
    queryset1=Goals.objects.filter(appraisal = selfappraisal, employee = selfappraisal.employee)

    if request.method == 'POST' and 'send' in request.POST:
        formset = GoalsFormset(request.POST or None, queryset = queryset1)
        if formset.is_valid():
            goals = formset.save(commit=False)
            for goal in goals:
                goal.save()  
            
            return HttpResponseRedirect(reverse('user_homepage')) 

    else:
        formset = GoalsFormset(queryset = queryset1)

    context ={
        "goals_formset": formset,
        "employee_appraisal": selfappraisal
    }
    return render(request, 'Appraisals/MidUpdateG.html', context)

@login_required(login_url='login')
def UpdateMidAppraisalG_M(request, *args, **kwargs):
    id = kwargs.get('pk')
    selfappraisal = get_object_or_404(User_Appraisal_List, id=id)

    context ={
        "employee_appraisal": selfappraisal
    }
    return render(request, 'Appraisals/MidUpdateG.html', context)


@login_required(login_url='login')
def UpdateAppraisalG(request, *args, **kwargs):
    id = kwargs.get('pk')
    selfappraisal = get_object_or_404(User_Appraisal_List, id=id)

    context ={
        "employee_appraisal": selfappraisal
    }
    return render(request, 'Appraisals/HuNet_UpdateG.html', context)

@login_required(login_url='login')
def UpdateAppraisalC(request, *args, **kwargs):
    id = kwargs.get('pk')
    selfappraisal = get_object_or_404(User_Appraisal_List, id=id)
    sum = 0
    weightage_count = 0

    context ={
        "employee_appraisal": selfappraisal
    }
    return render(request, 'Appraisals/HuNet_UpdateC.html', context)

@login_required(login_url='login')
def Update_Appraisal(request, *args, **kwargs):
    id = kwargs.get('pk')
    selfappraisal = User_Appraisal_List.objects.get(id=id)
    overallappraisal = selfappraisal.overall_appraisal    
    
    #Goals
   
    context={
        'user_app': selfappraisal,
    }
    return render(request, 'Appraisals/HuNet_UpdateUAL.html', context)

@login_required(login_url='login')
def createCareerDiscussion(request, *args, **kwargs):
    id = kwargs.get('pk')
    user_appraisal_list = User_Appraisal_List.objects.get(id=id)
    overall_appraisal = user_appraisal_list.overall_appraisal
    
    final_score = FINAL_GRADE(user_appraisal_list, overall_appraisal)
    final_grade = GRADING_SYSTEM(final_score)

    form = CreateCareerDiscussionForm2(request.POST or None)
    if form.is_valid(): 
        careerdiscussion = form.save(commit=False)
        careerdiscussion.employee = request.user.profile
        careerdiscussion.user_appraisal = user_appraisal_list
        careerdiscussion.save()
        return redirect('../Update/')
            
    context={
        'form': form,
        'grade': final_grade,
        'user_app': user_appraisal_list
        }
    return render(request, 'Appraisals/HuNet_UpdateCD.html', context)

@method_decorator(login_required(login_url='login'), name='dispatch')
class Update_Appraisal2(UpdateView):
    model = User_Appraisal_List
    fields = []
    success_url = reverse_lazy('user_homepage')
    template_name = 'Appraisals/HuNet_UpdateUAL.html'

    def form_valid(self, form):
        form.instance.completion = 'ECompleted'
        print(form.cleaned_data)
        return super(Update_Appraisal2, self).form_valid(form)

@login_required(login_url='login')
def UpdateAppraisalS(request, *args, **kwargs):
    id = kwargs.get('pk')
    selfappraisal = get_object_or_404(User_Appraisal_List, id=id)

    skills_count = selfappraisal.skills_set.count()

    SkillsFormset=modelformset_factory(Skills, form = AppSkillsForm, extra = 0)
    queryset1=Skills.objects.filter(appraisal = selfappraisal, employee = selfappraisal.employee)
    
    weightage_count = 0
    sum = 0

    if request.method == 'POST' and 'send' in request.POST:
        formset = SkillsFormset(request.POST or None, queryset = queryset1)
        if formset.is_valid():
            skills = formset.save(commit=False)
            for skill in skills:
                skill.save()  
            return HttpResponseRedirect(reverse('Appraisals:Update_AppraisalCareer', args=(id,))) 

    elif request.method == 'POST' and 'calculate' in request.POST:
        formset = SkillsFormset(request.POST or None, queryset = queryset1)
        if formset.is_valid():
            skills = formset.save(commit=False)
            for skill in skills:
                skill.save()  
            for skill in selfappraisal.skills_set.all():
                weightage_count+=skill.weightage
            for skill in selfappraisal.skills_set.all():
                sum+=skill.user_rating * skill.weightage / weightage_count
            avg = sum
            sum = 0
            weightage_count = 0

            if avg >= 5:
                messages.info(request,'Average Rating: '+ str(round(avg,1)))
                messages.info(request,'Grade: Far Exceed Expectations')
            
            elif avg >= 4:
                messages.info(request,'Average Rating: '+ str(round(avg,1)))
                messages.info(request,'Grade: Exceeds Expectations')

            elif avg >= 3:
                messages.info(request,'Average Rating: '+ str(round(avg,1)))
                messages.info(request,'Grade: Meets Expectations')

            elif avg >= 2:
                messages.info(request,'Average Rating: '+ str(round(avg,1)))
                messages.info(request,'Grade: Needs Improvement')

            elif avg >= 1:
                messages.info(request,'Average Rating: '+ str(round(avg,1)))
                messages.info(request,'Grade: Major Improvement needed')
            return redirect('.')
 
        
    else:
        formset = SkillsFormset(queryset = queryset1)


    context ={
        "skills_formset": formset,
        "employee_appraisal": selfappraisal,
        "skills_count": skills_count
    }
    return render(request, 'Appraisals/HuNet_UpdateS.html', context) 

@login_required(login_url='login')
def UpdateAppraisalG_M(request, *args, **kwargs):
    id = kwargs.get('pk')
    selfappraisal = get_object_or_404(User_Appraisal_List, id=id)

    context ={
        "employee_appraisal": selfappraisal
    }
    return render(request, 'Appraisals/HuNetM_UpdateG.html', context)

@login_required(login_url='login')
def UpdateAppraisalC_M(request, *args, **kwargs):
    id = kwargs.get('pk')
    selfappraisal = get_object_or_404(User_Appraisal_List, id=id)

    context ={
        "employee_appraisal": selfappraisal
    }
    return render(request, 'Appraisals/HuNetM_UpdateC.html', context)

@login_required(login_url='login')
def UpdateAppraisalS_M(request, *args, **kwargs):
    id = kwargs.get('pk')
    selfappraisal = get_object_or_404(User_Appraisal_List, id=id)

    skills_count = selfappraisal.skills_set.count()

    context ={
        "employee_appraisal": selfappraisal,
    }
    return render(request, 'Appraisals/HuNetM_UpdateS.html', context)

@login_required(login_url='login')
def UpdateAppraisalCareer_M(request, *args, **kwargs):
    id = kwargs.get('pk')
    user_appraisal_list = User_Appraisal_List.objects.get(id=id)
    overall_appraisal = user_appraisal_list.overall_appraisal
    car_discussion = user_appraisal_list.career_discussion_set.order_by('-id')[0]

    final_score = M_FINAL_GRADE(user_appraisal_list, overall_appraisal)
    final_grade = GRADING_SYSTEM(final_score)

      
    context={
        'grade': final_grade,
        'user_app': user_appraisal_list
        }
    return render(request, 'Appraisals/HuNetM_UpdateCD.html', context)

@login_required(login_url='login')
def Update_Appraisal_M(request, *args, **kwargs):
    id = kwargs.get('pk')
    selfappraisal = User_Appraisal_List.objects.get(id=id)
    overallappraisal = selfappraisal.overall_appraisal    
    
    #Goals
    sum = 0
    weightage_count=0
    totalsum = 0
    for goal in selfappraisal.goals_set.all():
        weightage_count+=goal.weightage
    for goal in selfappraisal.goals_set.all():
        sum+=goal.manager_rating * goal.weightage / weightage_count
    totalsum += sum * overallappraisal.goal_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)
    avg1 = round(sum,1)

    sum = 0
    weightage_count = 0
    for competency in selfappraisal.competencies_set.all():
        weightage_count+=competency.weightage
    for competency in selfappraisal.competencies_set.all():
        sum+=competency.manager_rating * competency.weightage / weightage_count
    totalsum += sum * overallappraisal.competency_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)
    avg2 = round(sum,1)

    sum = 0
    weightage_count = 0
    for skill in selfappraisal.skills_set.all():
        weightage_count+=skill.weightage
    for skill in selfappraisal.skills_set.all():
        sum+=skill.manager_rating * skill.weightage / weightage_count
    totalsum += sum * overallappraisal.skill_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)
    avg3 = round(sum,1)

    totalavg = round(totalsum,1)

    avg1_grade = GRADING_SYSTEM(avg1)
    avg2_grade = GRADING_SYSTEM(avg2)
    avg3_grade = GRADING_SYSTEM(avg3)
    totalavg_grade = GRADING_SYSTEM(totalavg)


    form = UpdateManagerAppRatingForm(request.POST or None, instance = selfappraisal)
    if form.is_valid():
        user_app = form.save(commit=False)
        user_app.completion = 'MCompleted'
        user_app.save()
        return HttpResponseRedirect(reverse('user_homepage'))

    context={
        'user_app': selfappraisal,
        'goals_score': avg1,
        'competencies_score': avg2,
        'skills_score': avg3,
        'total_score': totalavg,
        'goals_weightage': avg1_grade,
        'competencies_weightage': avg2_grade,
        'skills_weightage': avg3_grade,
        'total_weightage': totalavg_grade,
        'form': form
    }
    return render(request, 'Appraisals/HuNetM_UpdateUAL.html', context)

@login_required(login_url='login')
def UpdateAppraisalG_B(request, *args, **kwargs):
    id = kwargs.get('pk')
    selfappraisal = get_object_or_404(User_Appraisal_List, id=id)

    context ={
        "employee_appraisal": selfappraisal
    }
    return render(request, 'Appraisals/HuNetB_UpdateG.html', context)

@login_required(login_url='login')
def UpdateAppraisalC_B(request, *args, **kwargs):
    id = kwargs.get('pk')
    selfappraisal = get_object_or_404(User_Appraisal_List, id=id)

    context ={
        "employee_appraisal": selfappraisal
    }
    return render(request, 'Appraisals/HuNetB_UpdateC.html', context)

@login_required(login_url='login')
def UpdateAppraisalS_B(request, *args, **kwargs):
    id = kwargs.get('pk')
    selfappraisal = get_object_or_404(User_Appraisal_List, id=id)

    skills_count = selfappraisal.skills_set.count()

 
    context ={
        "skills_formset": formset,
        "skills_count": skills_count
    }
    
    return render(request, 'Appraisals/HuNetB_UpdateS.html', context)

@login_required(login_url='login')
def UpdateAppraisalCareer_B(request, *args, **kwargs):
    id = kwargs.get('pk')
    user_appraisal_list = User_Appraisal_List.objects.get(id=id)
    overall_appraisal = user_appraisal_list.overall_appraisal
    car_discussion = user_appraisal_list.career_discussion_set.order_by('-id')[0]

    final_score = B_FINAL_GRADE(user_appraisal_list, overall_appraisal)
    final_grade = GRADING_SYSTEM(final_score)

    if request.method == 'POST':
        return HttpResponseRedirect(reverse('Appraisals:Update_Appraisal_B', args=(id,)))  

    context={
        'grade': final_grade,
        'user_app': user_appraisal_list,
        'user_career_discussion': car_discussion 
        }
    return render(request, 'Appraisals/HuNetB_UpdateCD.html', context)

@login_required(login_url='login')
def Update_Appraisal_B(request, *args, **kwargs):
    id = kwargs.get('pk')
    selfappraisal = User_Appraisal_List.objects.get(id=id)
    overallappraisal = selfappraisal.overall_appraisal    
    
    #Goals
    sum = 0
    weightage_count=0
    totalsum = 0
    for goal in selfappraisal.goals_set.all():
        weightage_count+=goal.weightage
    for goal in selfappraisal.goals_set.all():
        sum+=goal.board_rating * goal.weightage / weightage_count
    totalsum += sum * overallappraisal.goal_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)
    avg1 = round(sum,1)

    sum = 0
    weightage_count = 0
    for competency in selfappraisal.competencies_set.all():
        weightage_count+=competency.weightage
    for competency in selfappraisal.competencies_set.all():
        sum+=competency.board_rating * competency.weightage / weightage_count
    totalsum += sum * overallappraisal.competency_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)
    avg2 = round(sum,1)

    sum = 0
    weightage_count = 0
    for skill in selfappraisal.skills_set.all():
        weightage_count+=skill.weightage
    for skill in selfappraisal.skills_set.all():
        sum+=skill.board_rating * skill.weightage / weightage_count
    totalsum += sum * overallappraisal.skill_weightage / (overallappraisal.goal_weightage + overallappraisal.competency_weightage + overallappraisal.skill_weightage)
    avg3 = round(sum,1)

    totalavg = round(totalsum,1)

    avg1_grade = GRADING_SYSTEM(avg1)
    avg2_grade = GRADING_SYSTEM(avg2)
    avg3_grade = GRADING_SYSTEM(avg3)
    totalavg_grade = GRADING_SYSTEM(totalavg)


    form = UpdateBoardAppRatingForm(request.POST or None, instance = selfappraisal)
    if form.is_valid():
        user_app = form.save(commit=False)
        user_app.completion = 'BCompleted'
        user_app.save()
        return HttpResponseRedirect(reverse('user_homepage'))

    context={
        'user_app': selfappraisal,
        'goals_score': avg1,
        'competencies_score': avg2,
        'skills_score': avg3,
        'total_score': totalavg,
        'goals_weightage': avg1_grade,
        'competencies_weightage': avg2_grade,
        'skills_weightage': avg3_grade,
        'total_weightage': totalavg_grade,
        'form': form
    }
    return render(request, 'Appraisals/HuNetB_UpdateUAL.html', context)

@method_decorator(login_required(login_url='login'), name='dispatch')
class Update_Appraisal2_B(UpdateView):
    model = User_Appraisal_List
    form_class = BAppForm
    success_url = reverse_lazy('user_homepage')
    template_name = 'Appraisals/HuNetB_UpdateUAL.html'

    def form_valid(self, form):
        form.instance.completion = 'BCompleted'
        print(form.cleaned_data)
        return super(Update_Appraisal2_B, self).form_valid(form)

#Real one
@login_required(login_url='login')
def Add_User_Appraisal_Indiv(request, *args, **kwargs):
    id=kwargs.get('pk')
    overall_appraisal = Overall_Appraisal.objects.get(id=id)
    profile_database = Profile.objects.all().order_by('name')

    form_class = TryingOutForm

    # list_of_emails = []

    if request.method == 'POST':        
        formset = form_class(request.POST)

        try:
            list_of_ids = request.POST.getlist('profile_list')
            user_profile2 = Profile.objects.get(id=list_of_ids[0])
        except:
            pass

        for i in range(len(list_of_ids)):
            user_profile2 = Profile.objects.get(id=list_of_ids[i])
            updated_data = request.POST.copy()
            updated_data.update({'employee':user_profile2})
            formset = form_class(updated_data)
            if formset.is_valid():
                instance = formset.save(commit = False)

                instance.employee = user_profile2
                instance.manager = user_profile2.first_Reporting_Manager
                instance.overall_appraisal = overall_appraisal
                instance.status = 'Employee'
                instance.appraisal_name = overall_appraisal.name
                instance.appraisal_category = overall_appraisal.appraisal_category
                instance.start_date = overall_appraisal.start_date
                instance.end_date = overall_appraisal.calibration_end_date                
                instance.completion = 'null'
                # list_of_emails.append(user_profile2)
                instance.save()

        # notification = "Dear Users, \n\n The Performance Appraisal Exercise has started! \n\n Please see the datelines for the various stages below: \n " + "+1"
        # if len(list_of_emails) >= 0:
        #     send_mail('Creation of Overall Appraisal', 'Hi! \n\t An Overall Appraisal have been launched and you are in it!', from_email = 'bennyteomh@gmail.com', recipient_list=[list_of_emails], fail_silently=True)

        return HttpResponseRedirect(reverse('Appraisals:Create_Overall_Appraisal_Stage3', args=(overall_appraisal.id,)))

    context={
        'profile_list': profile_database
    }
    return render(request, 'Appraisals/Create_UALForm_Indiv.html', context)

@login_required(login_url='login')
def Add_User_Appraisal_Dept(request, *args, **kwargs):
    id=kwargs.get('pk')
    overall_appraisal = Overall_Appraisal.objects.get(id=id)
    department_database = Departments.objects.all().order_by('name')

    form_class = TryingOutForm

    if request.method == 'POST':        
        formset = form_class(request.POST)

        try:
            list_of_dept = request.POST.getlist('department_list')
        except:
            pass

        for i in range(len(list_of_dept)):
            dept_profiles = Profile.objects.filter(department=list_of_dept[i])

            for x in range(len(dept_profiles)):
                user_profile = dept_profiles[x]
                updated_data = request.POST.copy()
                updated_data.update({'employee':user_profile})
                formset = form_class(updated_data)
                if formset.is_valid():
                    instance = formset.save(commit = False)

                    instance.employee = user_profile
                    instance.manager = user_profile.first_Reporting_Manager
                    instance.overall_appraisal = overall_appraisal
                    instance.status = 'Employee'
                    instance.appraisal_name = overall_appraisal.name
                    instance.appraisal_category = overall_appraisal.appraisal_category
                    instance.start_date = overall_appraisal.start_date
                    instance.end_date = overall_appraisal.calibration_end_date
                    instance.completion = 'null'
                    instance.save()

        return HttpResponseRedirect(reverse('Appraisals:Create_Overall_Appraisal_Stage3', args=(overall_appraisal.id,)))

    context={
        'department_list': department_database
    }
    return render(request, 'Appraisals/Create_UALForm_Dept.html', context)

@login_required(login_url='login')
def Add_User_Appraisal_Company(request, *args, **kwargs):
    id=kwargs.get('pk')
    overall_appraisal = Overall_Appraisal.objects.get(id=id)

    return HttpResponseRedirect(reverse('Appraisals:Create_Overall_Appraisal_Stage3', args=(overall_appraisal.id,)))

    context={
    }
    return render(request, 'Appraisals/Create_UALForm_Company.html', context)

#Useless but I need for ref :3
@login_required(login_url='login')
def Add_User_Appraisal123(request, *args, **kwargs):
    UserAppFormSet = inlineformset_factory(Overall_Appraisal, User_Appraisal_List, fields=('employee',), extra=15 )
    id=kwargs.get('pk')
    overall_appraisal = Overall_Appraisal.objects.get(id=id)
    

    formset = UserAppFormSet(queryset=User_Appraisal_List.objects.none(), instance = overall_appraisal)

    if request.method == 'POST':
        formset = UserAppFormSet(request.POST, instance=overall_appraisal)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.manager = instance.employee.first_Reporting_Manager
                instance.overall_appraisal = overall_appraisal
                instance.status = 'Employee'
                instance.appraisal_name = overall_appraisal.name
                instance.appraisal_category = overall_appraisal.appraisal_category
                instance.start_date = overall_appraisal.start_date
                instance.end_date = overall_appraisal.calibration_end_date
                instance.completion = 'null'
            formset.save()
            return redirect('../../../hrhome/')
    
    context={'formset': formset}
    return render(request, 'Appraisals/Create_UALForm.html', context)

@login_required(login_url='login')
def Create_Peer_Appraisal(request, *args, **kwargs):
    
    personal_profile = Profile.objects.get(user = request.user)
    subordinate_profile_database = personal_profile.profile_set.all()
    company_profile_database = Profile.objects.exclude(first_Reporting_Manager = personal_profile)

    form = CreatePeerAppraisalForm

    if request.method == 'POST':        
        form = CreatePeerAppraisalForm(request.POST)
        
        try:
            list_of_ids = request.POST.getlist('profile_list')
            user_profile = Profile.objects.get(id=list_of_ids[0])
        except IndexError:
            print("Index not in range")
        

        try:
            list_of_ids2 = request.POST.getlist('profile_list2')
            user_profile2 = Profile.objects.get(id=list_of_ids2[0])
        except IndexError:
            print("Index not in range")
        

        if len(list_of_ids) >= 1:
            for i in range(len(list_of_ids)):
                user_profile = Profile.objects.get(id=list_of_ids[i])
                updated_data = request.POST.copy()
                updated_data.update({'viewer':user_profile,})
                form = CreatePeerAppraisalForm(updated_data)
                if form.is_valid():
                    peerApp = form.save(commit = False)

                    peerApp.manager = peerApp.appraisal.employee.first_Reporting_Manager
                    peerApp.completion = 'Uncompleted'
                    peerApp.created_by = personal_profile
                    peerApp.save()
        
        else:
            pass
        
        if len(list_of_ids2) >= 1:
            for i in range(len(list_of_ids2)):
                user_profile2 = Profile.objects.get(id=list_of_ids2[i])
                updated_data = request.POST.copy()
                updated_data.update({'viewer':user_profile2,})
                form = CreatePeerAppraisalForm(updated_data)
                if form.is_valid():
                    peerApp = form.save(commit = False)

                    peerApp.manager = peerApp.appraisal.employee.first_Reporting_Manager
                    peerApp.completion = 'Uncompleted'
                    peerApp.created_by = personal_profile
                    peerApp.save()
        else:
            pass

        return HttpResponseRedirect(reverse('user_homepage'))

    context={
        'subordinate_profile_database': subordinate_profile_database,
        'subordinate_exclusion_database' : company_profile_database,
        'form': form
    }
    return render(request, 'Appraisals/Create_PeerAppraisal.html', context)

@login_required(login_url='login')
def Update_Peer_Appraisal(request, *args, **kwargs):
    id = kwargs.get('pk')
    peer_appraisal = peerAppraisal.objects.get(id=id)

    form = UpdatePeerAppraisalForm(request.POST or None, instance = peer_appraisal)
    if form.is_valid():
        peerApp = form.save(commit=False)
        peerApp.completion = 'Completed'
        peerApp.save()
        return HttpResponseRedirect(reverse('user_homepage'))
    
    context={
        'form': form,
        'peer_appraisal': peer_appraisal
    }
    return render(request, 'Appraisals/Update_PeerAppraisal.html', context)

@login_required(login_url='login')
def create_Overall_Appraisal_Stage1(request):
    form = CreateOverallAppraisalForm_Stage1(request.POST or None)
    employee_selection = request.POST.get('employee_selection_list')
    if form.is_valid():
        overall_app = form.save(commit=False)

        if 'Individual' in employee_selection:
            overall_app.save()
            return HttpResponseRedirect(reverse('Appraisals:Invite_Indiv_User_Appraisal', args=(overall_app.id,)))
        elif 'Department' in employee_selection:
            overall_app.save()
            return HttpResponseRedirect(reverse('Appraisals:Invite_Dept_User_Appraisal', args=(overall_app.id,)))
        elif 'Company' in employee_selection:
            overall_app.save()
            return HttpResponseRedirect(reverse('Appraisals:Invite_Company_User_Appraisal', args=(overall_app.id,)))
        return HttpResponseRedirect(reverse('Appraisals:Create_Overall_Appraisal1'))

    context={
        'form': form
    }
    return render(request, 'Appraisals/HuNet_CreateOverallApp_Stage1.html', context)

@login_required(login_url='login')
def create_Overall_Appraisal_Stage3(request, *args, **kwargs):
    id = kwargs.get('pk')
    overall_app = Overall_Appraisal.objects.get(id = id)

    form = CreateOverallAppraisalForm_Stage3(request.POST or None, instance=overall_app)
    if form.is_valid():
        overall_app = form.save(commit=False)
        if (overall_app.start_date > overall_app.goals_setting_end_date):
            messages.warning(request, 'Goals Setting Start Date can not start later than its End Date')
            return HttpResponseRedirect(reverse('Appraisals:Create_Overall_Appraisal_Stage3', args=(overall_app.id,)))

        elif (overall_app.goals_setting_end_date > overall_app.mid_year_start_date):
            messages.warning(request, 'Goals Setting End Date can not start later than the Mid-Year Start Date')
            return HttpResponseRedirect(reverse('Appraisals:Create_Overall_Appraisal_Stage3', args=(overall_app.id,)))

        elif (overall_app.mid_year_start_date > overall_app.mid_year_end_date):
            messages.warning(request, 'Mid-Year Rating Start Date can not start later than its End Date')
            return HttpResponseRedirect(reverse('Appraisals:Create_Overall_Appraisal_Stage3', args=(overall_app.id,)))

        elif (overall_app.mid_year_end_date > overall_app.end_year_start_date):
            messages.warning(request, 'Mid-Year Rating End Date can not start later than the End-Year Start Date')
            return HttpResponseRedirect(reverse('Appraisals:Create_Overall_Appraisal_Stage3', args=(overall_app.id,)))

        elif (overall_app.end_year_start_date > overall_app.appraisal_end_date):
            messages.warning(request, 'End-Year Start Date can not start later than its Ratings End Date')
            return HttpResponseRedirect(reverse('Appraisals:Create_Overall_Appraisal_Stage3', args=(overall_app.id,)))

        elif (overall_app.appraisal_end_date > overall_app.reports_end_date):
            messages.warning(request, 'End-Year Rating End Date can not start later than its Moderation-by-Management End Date')
            return HttpResponseRedirect(reverse('Appraisals:Create_Overall_Appraisal_Stage3', args=(overall_app.id,)))

        elif (overall_app.reports_end_date > overall_app.calibration_end_date):
            messages.warning(request, 'End-Year Moderation-by-Management End Date can not start later than its Calibration End Date')
            return HttpResponseRedirect(reverse('Appraisals:Create_Overall_Appraisal_Stage3', args=(overall_app.id,)))

        form.save()

        return HttpResponseRedirect(reverse('Appraisals:Create_Overall_Appraisal_Stage4', args=(overall_app.id,)))

    context={
        'form': form
    }
    return render(request, 'Appraisals/HuNet_CreateOverallApp_Stage3.html', context)

@login_required(login_url='login')
def create_Overall_Appraisal_Stage4(request, *args, **kwargs):
    id = kwargs.get('pk')
    overall_appraisal = Overall_Appraisal.objects.get(id=id)

    list_of_emails=[]
    user_appraisal_data = User_Appraisal_List.objects.filter(overall_appraisal = overall_appraisal)
    for user_appraisal_indiv in user_appraisal_data:
        list_of_emails.append(user_appraisal_indiv.employee.email)
    email_string = APPRAISAL_LAUNCHING_EMAIL(overall_appraisal)

    form = CreateOverallAppraisalForm_Stage4(request.POST or None, instance = overall_appraisal)
    if form.is_valid():
        overall_app = form.save(commit=False)
        if (overall_app.goal_weightage + overall_app.competency_weightage + overall_app.skill_weightage != 100):
            messages.warning(request, 'Goal, Competency and Skill weightage does not add up to 100%')
            return HttpResponseRedirect(reverse('Appraisals:Create_Overall_Appraisal_Stage4', args=(overall_appraisal.id,)))
        overall_app.rating_scale = 'Denselight System'
        overall_app.status = 'Stage 1'
        overall_app.save()
        if len(list_of_emails) > 0:
            send_mail('The Performance Appraisal Exercise has started!', email_string, from_email = 'denselight_epmp@consulthunet.com', recipient_list=list_of_emails, fail_silently=True)
        return HttpResponseRedirect(reverse('user_homepage'))

    context={
        'form': form
    }
    return render(request, 'Appraisals/HuNet_CreateOverallApp_Stage4.html', context)

@login_required(login_url='login')
def create_Overall_Appraisal_Ref(request):
    form = CreateOverallAppraisalForm_Stage3(request.POST or None)
    employee_selection = request.POST.get('employee_selection_list')
    if form.is_valid():
        overall_app = form.save(commit=False)
        if (overall_app.goal_weightage + overall_app.competency_weightage + overall_app.skill_weightage != 100):
            messages.warning(request, 'Goal, Competency and Skill weightage does not add up to 100%')
            return HttpResponseRedirect(reverse('Appraisals:Create_Overall_Appraisal1'))

        if 'Individual' in employee_selection:
            overall_app.save()
            return HttpResponseRedirect(reverse('Appraisals:Invite_Indiv_User_Appraisal', args=(overall_app.id,)))
        elif 'Department' in employee_selection:
            overall_app.save()
            return HttpResponseRedirect(reverse('Appraisals:Invite_Dept_User_Appraisal', args=(overall_app.id,)))
        elif 'Company' in employee_selection:
            overall_app.save()
            return HttpResponseRedirect(reverse('Appraisals:Invite_Company_User_Appraisal', args=(overall_app.id,)))
        return HttpResponseRedirect(reverse('Appraisals:Create_Overall_Appraisal1'))

    context={
        'form': form
    }
    return render(request, 'Appraisals/HuNet_CreateOverallApp_Stage4.html', context)

@login_required(login_url='login')
def update_Overall_Appraisal(request, *args, **kwargs):
    id = kwargs.get('pk')
    overall_appraisal = Overall_Appraisal.objects.get(id=id)

    email_string = ""
    listOfEmails = []
    for userappraisal in overall_appraisal.user_appraisal_list_set.all():
        try:
            listOfEmails.append(userappraisal.employee.email)
        except Exception:
            pass

    form = UpdateOverallAppraisalForm(request.POST or None, instance = overall_appraisal)
    if form.is_valid():
        overall_app = form.save(commit=False)
        if (overall_app.goal_weightage + overall_app.competency_weightage + overall_app.skill_weightage != 100):
            messages.warning(request, 'Goal, Competency and Skill weightage does not add up to 100%')
            return HttpResponseRedirect(reverse('user_homepage'))
        overall_app.save()

        if overall_app.status == 'Stage 1':
            try:
                email_string = APPRAISAL_LAUNCHING_EMAIL(overall_app)
                send_mail('Initialisation of Performance Appraisal Launch', email_string, from_email = 'denselight_epmp@consulthunet.com', recipient_list=listOfEmails, fail_silently=True)
            except Exception:
                pass

        elif overall_app.status == 'Stage 1B':
            try:
                email_string = MID_YEAR_REVIEW_EMAIL(str(overall_app.mid_year_end_date))
                send_mail('Mid-Year Review has started!', email_string, from_email = 'denselight_epmp@consulthunet.com', recipient_list=listOfEmails, fail_silently=True)
            except Exception:
                pass 
        elif overall_app.status == 'Stage 2':
            try:
                email_string = YEAR_END_REVIEW_EMAIL(str(overall_app.mid_year_end_date))
                send_mail('Year-End Review has started!', email_string, from_email = 'denselight_epmp@consulthunet.com', recipient_list=listOfEmails, fail_silently=True)
            except Exception:
                pass 
        return HttpResponseRedirect(reverse('user_homepage'))

    context={
        'form': form
    }
    return render(request, 'Appraisals/HuNet_UpdateOverallApp.html', context)

@method_decorator(login_required(login_url='login'), name='dispatch')
class update_MID_Overall_Appraisal(UpdateView):
    model = Overall_Appraisal
    fields = []
    success_url = reverse_lazy('user_homepage')
    template_name = 'Appraisals/Update_MtS2E_UAL.html'

    def form_valid(self, form):
        form.instance.mid_year_stage = 'Completed'
        print(form.cleaned_data)
        return super(update_MID_Overall_Appraisal, self).form_valid(form)

@login_required(login_url='login')
def PersonalAppraisalReport(request, *args, **kwargs):
    id = kwargs.get('pk')
    user_overall_appraisal = Overall_Appraisal.objects.get(id=id)
    _id = kwargs.get('mk')
    user_user_appraisal = User_Appraisal_List.objects.get(id=_id)
    profile_id = kwargs.get('dk')
    user_profile = Profile.objects.get(id=profile_id)
    context={
        'overall_appraisal_database': user_overall_appraisal,
        'user_appraisal_database': user_user_appraisal,
        'profile_database':user_profile
    }
    return render(request, 'Appraisals/Report_PersonalOverall.html', context)

@login_required(login_url='login')
def export_PersonalAppraisalReport(request, *args, **kwargs):
    id = kwargs.get('pk')
    user_appraisal = User_Appraisal_List.objects.get(id=id)
    overall_appraisal = user_appraisal.overall_appraisal

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Name','Department', 'Email', 'Job Title',"Manager's Name",'Goals Count','Core Values Competencies Count','Skills Count',"Employee's Rating","Manager's Rating","Board's Rating",'Rewards Recommendations','Training & Development Recommendations(Employee)','Training & Development Recommendations(Manager)','Training & Development Recommendations(Board)', "Employee's Comments (Goals)", "Employee's Comments (Competencies)", "Employee's Comments (Skills)", "Manager's Comments (Goals)", "Manager's Comments (Competencies)", "Manager's Comments (Skills)",  "Board's Comments (Goals)", "Board's Comments (Competencies)", "Board's Comments (Skills)",])
    
    name=""
    department=""
    email=""
    job_title=""
    manager_name = ""
    
    name += user_appraisal.employee.name
    department += user_appraisal.employee.department.name
    email += user_appraisal.employee.email
    job_title += user_appraisal.employee.job_Title
    manager_name += user_appraisal.employee.first_Reporting_Manager.name

    comment_counter = 0
    goals_employees_comments = ""
    goals_manager_comments = ""
    goals_board_comments = ""

    competencies_employees_comments = ""
    competencies_manager_comments = ""
    competencies_board_comments = ""

    skills_employees_comments = ""
    skills_manager_comments = ""
    skills_board_comments = ""

    all_employees_TDR = ""
    all_managers_TDR = ""
    all_board_TDR = ""

    rewards_recommendation_manager = 'Increment: ' + str(user_appraisal.incrementRecommendation) + '% | Bonus: ' + str(user_appraisal.bonusRecommendation)

    goals_count = user_appraisal.goals_set.count()
    competencies_count = user_appraisal.competencies_set.count()
    skills_count = user_appraisal.skills_set.count()

    employee_rating = 0
    manager_rating = 0
    board_rating = 0
        
    try:
        employee_rating = FINAL_GRADE(user_appraisal, overall_appraisal)
    except Exception:
        pass

    try:
        manager_rating = M_FINAL_GRADE(user_appraisal, overall_appraisal)
    except Exception:
        pass

    try:
        board_rating = B_FINAL_GRADE(user_appraisal, overall_appraisal)
    except Exception:
        pass

    for goals in user_appraisal.goals_set.all():
        comment_counter += 1
        goals_employees_comments += "G" + str(comment_counter) + ". " + goals.user_comments + "| "
        goals_manager_comments += "G" + str(comment_counter) + ". " + goals.manager_comments + "| "
        goals_board_comments += "G" + str(comment_counter) + ". " + goals.board_comments + "| "
    comment_counter=0
        
    for competencies in user_appraisal.competencies_set.all():
        comment_counter += 1
        competencies_employees_comments += "C" + str(comment_counter) + ". " +competencies.user_comments + "| "
        competencies_manager_comments += "C" + str(comment_counter) + ". " +competencies.manager_comments + "| "
        competencies_board_comments += "C" + str(comment_counter) + ". " +competencies.board_comments + "| "
    comment_counter=0

    for skills in user_appraisal.skills_set.all():
        comment_counter += 1

        skills_employees_comments += "S" + str(comment_counter) + ". " + skills.user_comments + "| "
        skills_manager_comments += "S" + str(comment_counter) + ". " + skills.manager_comments + "| "
        skills_board_comments += "S" + str(comment_counter) + ". " + skills.board_comments + "| "

        all_employees_TDR += "S" + str(comment_counter) + ". " + skills.recommended_Trainings_user + "| "
        all_managers_TDR += "S" + str(comment_counter) + ". " + skills.recommended_Trainings_manager + "| "
        all_board_TDR += "S" + str(comment_counter) + ". " + skills.recommended_Trainings_board + "| "

    comment_counter=0

    writer.writerow([name, department, email, job_title, manager_name, goals_count, competencies_count, skills_count, employee_rating, manager_rating, board_rating, rewards_recommendation_manager, all_employees_TDR, all_managers_TDR, all_board_TDR, goals_employees_comments, goals_manager_comments, goals_board_comments, competencies_employees_comments, competencies_manager_comments, competencies_board_comments, skills_employees_comments, skills_manager_comments, skills_board_comments,])

        
    response['Content-Disposition'] = 'attachment; filename="Individual_Appraisal_Report.csv"'
    return response
    

@login_required(login_url='login')
def Comp_FinalAppReport(request, *args, **kwargs):
    id = kwargs.get('pk')
    report_overall_appraisal = Overall_Appraisal.objects.get(id=id)
    report_user_appraisal_list = User_Appraisal_List.objects.filter(overall_appraisal = report_overall_appraisal)

    context={
        'report_overall_appraisal_database': report_overall_appraisal,
        'report_user_appraisal_database': report_user_appraisal_list 
    }
    return render(request, 'Appraisals/Report_CompanyFAR.html', context)

@login_required(login_url='login')
def export_FinalAppraisalReport(request, *args, **kwargs):
    id = kwargs.get('pk')
    overall_appraisal = Overall_Appraisal.objects.get(id=id)

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Name','Department','Job Title',"Manager's Name",'Goals Count','Core Values Competencies Count','Skills Count',"Employee's Rating","Manager's Rating","Board's Rating",'Rewards Recommendations','Training & Development Recommendations(Employee)','Training & Development Recommendations(Manager)','Training & Development Recommendations(Board)', "Employee's Comments (Goals)", "Employee's Comments (Competencies)", "Employee's Comments (Skills)", "Manager's Comments (Goals)", "Manager's Comments (Competencies)", "Manager's Comments (Skills)",  "Board's Comments (Goals)", "Board's Comments (Competencies)", "Board's Comments (Skills)",])

    for user_appraisal in overall_appraisal.user_appraisal_list_set.all():

        name=""
        department=""
        email=""
        job_title=""
        manager_name = ""
        
        name += user_appraisal.employee.name
        department += user_appraisal.employee.department.name
        email += user_appraisal.employee.email
        job_title += user_appraisal.employee.job_Title
        manager_name += user_appraisal.employee.first_Reporting_Manager.name

        comment_counter = 0
        goals_employees_comments = ""
        goals_manager_comments = ""
        goals_board_comments = ""

        competencies_employees_comments = ""
        competencies_manager_comments = ""
        competencies_board_comments = ""

        skills_employees_comments = ""
        skills_manager_comments = ""
        skills_board_comments = ""

        all_employees_TDR = ""
        all_managers_TDR = ""
        all_board_TDR = ""

        rewards_recommendation_manager = 'Increment: ' + str(user_appraisal.incrementRecommendation) + '% | Bonus: ' + str(user_appraisal.bonusRecommendation)

        goals_count = user_appraisal.goals_set.count()
        competencies_count = user_appraisal.competencies_set.count()
        skills_count = user_appraisal.skills_set.count()

        employee_rating = 0
        manager_rating = 0
        board_rating = 0
        
        try:
            employee_rating = FINAL_GRADE(user_appraisal, overall_appraisal)
        except Exception:
            pass

        try:
            manager_rating = M_FINAL_GRADE(user_appraisal, overall_appraisal)
        except Exception:
            pass

        try:
            board_rating = B_FINAL_GRADE(user_appraisal, overall_appraisal)
        except Exception:
            pass

        for goals in user_appraisal.goals_set.all():
            comment_counter += 1
            goals_employees_comments += "G" + str(comment_counter) + ". " + goals.user_comments + "| "
            goals_manager_comments += "G" + str(comment_counter) + ". " + goals.manager_comments + "| "
            goals_board_comments += "G" + str(comment_counter) + ". " + goals.board_comments + "| "
        comment_counter=0
        
        for competencies in user_appraisal.competencies_set.all():
            comment_counter += 1
            competencies_employees_comments += "C" + str(comment_counter) + ". " + competencies.user_comments + "| "
            competencies_manager_comments += "C" + str(comment_counter) + ". " + competencies.manager_comments + "| "
            competencies_board_comments += "C" + str(comment_counter) + ". " + competencies.board_comments + "| "
        comment_counter=0

        for skills in user_appraisal.skills_set.all():
            comment_counter += 1
            skills_employees_comments += "S" + str(comment_counter) + ". " + skills.user_comments + "| "
            skills_manager_comments += "S" + str(comment_counter) + ". " + skills.manager_comments + "| "
            skills_board_comments += "S" + str(comment_counter) + ". " + skills.board_comments + "| "

            all_employees_TDR += "S" + str(comment_counter) + ". " + skills.recommended_Trainings_user + "| "
            all_managers_TDR += "S" + str(comment_counter) + ". " + skills.recommended_Trainings_manager + "| "
            all_board_TDR += "S" + str(comment_counter) + ". " + skills.recommended_Trainings_board + "| "
        comment_counter=0

        writer.writerow([name, department, job_title, manager_name, goals_count, competencies_count, skills_count, employee_rating, manager_rating, board_rating, rewards_recommendation_manager, all_employees_TDR, all_managers_TDR, all_board_TDR, goals_employees_comments, goals_manager_comments, goals_board_comments, competencies_employees_comments, competencies_manager_comments, competencies_board_comments, skills_employees_comments, skills_manager_comments, skills_board_comments,])

        
    response['Content-Disposition'] = 'attachment; filename="Final_Appraisal_Report.csv"'
    return response
    
@login_required(login_url='login')
def Comp_FinalPayoutReport(request, *args, **kwargs):
    id = kwargs.get('pk')
    report_overall_appraisal = Overall_Appraisal.objects.get(id=id)
    report_user_appraisal_list = User_Appraisal_List.objects.filter(overall_appraisal = report_overall_appraisal)

    context={
        'report_overall_appraisal_database': report_overall_appraisal,
        'report_user_appraisal_database': report_user_appraisal_list 
    }
    return render(request, 'Appraisals/Report_CompanyFPR.html', context)

@login_required(login_url='login')
def export_FinalPayoutReport(request, *args, **kwargs):
    id = kwargs.get('pk')
    overall_appraisal = Overall_Appraisal.objects.get(id=id)

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Name','Department','Job Title',"Manager's Name",'Goals Count','Core Values Competencies Count','Skills Count',"Employee's Rating","Manager's Rating","Board's Rating",'Rewards Recommendations',])

    for user_appraisal in overall_appraisal.user_appraisal_list_set.all():

        name=""
        department=""
        email=""
        job_title=""
        manager_name = ""
        
        name += user_appraisal.employee.name
        department += user_appraisal.employee.department.name
        email += user_appraisal.employee.email
        job_title += user_appraisal.employee.job_Title
        manager_name += user_appraisal.employee.first_Reporting_Manager.name

        rewards_recommendation_manager = 'Bonus: ' + str(user_appraisal.bonusRecommendation)

        goals_count = user_appraisal.goals_set.count()
        competencies_count = user_appraisal.competencies_set.count()
        skills_count = user_appraisal.skills_set.count()

        employee_rating = 0
        manager_rating = 0
        board_rating = 0
        
        try:
            employee_rating = FINAL_GRADE(user_appraisal, overall_appraisal)
        except Exception:
            pass

        try:
            manager_rating = M_FINAL_GRADE(user_appraisal, overall_appraisal)
        except Exception:
            pass

        try:
            board_rating = B_FINAL_GRADE(user_appraisal, overall_appraisal)
        except Exception:
            pass
        

        writer.writerow([name, department, job_title, manager_name, goals_count, competencies_count, skills_count, employee_rating, manager_rating, board_rating, rewards_recommendation_manager,])

        
    response['Content-Disposition'] = 'attachment; filename="Final_Payout_Report.csv"'
    return response

@login_required(login_url='login')
def Comp_IncremRecommReport(request, *args, **kwargs):
    id = kwargs.get('pk')
    report_overall_appraisal = Overall_Appraisal.objects.get(id=id)
    report_user_appraisal_list = User_Appraisal_List.objects.filter(overall_appraisal = report_overall_appraisal)

    context={
        'report_overall_appraisal_database': report_overall_appraisal,
        'report_user_appraisal_database': report_user_appraisal_list 
    }
    return render(request, 'Appraisals/Report_CompanyIRR.html', context)

@login_required(login_url='login')
def export_IncremRecommReport(request, *args, **kwargs):
    id = kwargs.get('pk')
    overall_appraisal = Overall_Appraisal.objects.get(id=id)

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Name','Department','Job Title',"Manager's Name",'Goals Count','Core Values Competencies Count','Skills Count',"Employee's Rating","Manager's Rating","Board's Rating",'Rewards Recommendations',])

    for user_appraisal in overall_appraisal.user_appraisal_list_set.all():
        
        name=""
        department=""
        email=""
        job_title=""
        manager_name = ""
        
        name += user_appraisal.employee.name
        department += user_appraisal.employee.department.name
        email += user_appraisal.employee.email
        job_title += user_appraisal.employee.job_Title
        manager_name += user_appraisal.employee.first_Reporting_Manager.name

        comment_counter = 0

        rewards_recommendation_manager = 'Increment: ' + str(user_appraisal.incrementRecommendation) + '%'

        goals_count = user_appraisal.goals_set.count()
        competencies_count = user_appraisal.competencies_set.count()
        skills_count = user_appraisal.skills_set.count()

        employee_rating = 0
        manager_rating = 0
        board_rating = 0
        
        try:
            employee_rating = FINAL_GRADE(user_appraisal, overall_appraisal)
        except Exception:
            pass

        try:
            manager_rating = M_FINAL_GRADE(user_appraisal, overall_appraisal)
        except Exception:
            pass

        try:
            board_rating = B_FINAL_GRADE(user_appraisal, overall_appraisal)
        except Exception:
            pass

        writer.writerow([name, department, job_title, manager_name, goals_count, competencies_count, skills_count, employee_rating, manager_rating, board_rating, rewards_recommendation_manager,])

    response['Content-Disposition'] = 'attachment; filename="Increment_Recommendation_Report.csv"'
    return response

@login_required(login_url='login')
def Comp_TrainingRecommReport(request, *args, **kwargs):
    id = kwargs.get('pk')
    report_overall_appraisal = Overall_Appraisal.objects.get(id=id)
    report_user_appraisal_list = User_Appraisal_List.objects.filter(overall_appraisal = report_overall_appraisal)
        

    context={
        'report_overall_appraisal_database': report_overall_appraisal,
        'report_user_appraisal_database': report_user_appraisal_list 
    }
    return render(request, 'Appraisals/Report_CompanyTRR.html', context)

@login_required(login_url='login')
def export_TrainingRecommReport(request, *args, **kwargs):
    id = kwargs.get('pk')
    overall_appraisal = Overall_Appraisal.objects.get(id=id)

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Name','Department','Job Title',"Manager's Name",'Goals Count','Core Values Competencies Count','Skills Count',"Employee's Rating","Manager's Rating","Board's Rating",'Training & Development Recommendations(Employee)','Training & Development Recommendations(Manager)','Training & Development Recommendations(Board)', "Employee's Comments (Goals)", "Employee's Comments (Competencies)", "Employee's Comments (Skills)", "Manager's Comments (Goals)", "Manager's Comments (Competencies)", "Manager's Comments (Skills)",  "Board's Comments (Goals)", "Board's Comments (Competencies)", "Board's Comments (Skills)",])

    for user_appraisal in overall_appraisal.user_appraisal_list_set.all():

        name=""
        department=""
        email=""
        job_title=""
        manager_name = ""
        
        name += user_appraisal.employee.name
        department += user_appraisal.employee.department.name
        email += user_appraisal.employee.email
        job_title += user_appraisal.employee.job_Title
        manager_name += user_appraisal.employee.first_Reporting_Manager.name

        manager_name = ""
        if user_appraisal.employee.first_Reporting_Manager.name:
            manager_name += user_appraisal.employee.first_Reporting_Manager.name
        else:
            manager_name='NIL'

        comment_counter = 0
        goals_employees_comments = ""
        goals_manager_comments = ""
        goals_board_comments = ""

        competencies_employees_comments = ""
        competencies_manager_comments = ""
        competencies_board_comments = ""

        skills_employees_comments = ""
        skills_manager_comments = ""
        skills_board_comments = ""

        all_employees_TDR = ""
        all_managers_TDR = ""
        all_board_TDR = ""

        goals_count = user_appraisal.goals_set.count()
        competencies_count = user_appraisal.competencies_set.count()
        skills_count = user_appraisal.skills_set.count()

        employee_rating = 0
        manager_rating = 0
        board_rating = 0

        try:
            employee_rating = FINAL_GRADE(user_appraisal, overall_appraisal)
        except Exception:
            pass

        try:
            manager_rating = M_FINAL_GRADE(user_appraisal, overall_appraisal)
        except Exception:
            pass

        try:
            board_rating = B_FINAL_GRADE(user_appraisal, overall_appraisal)
        except Exception:
            pass

        for goals in user_appraisal.goals_set.all():
            comment_counter += 1
            goals_employees_comments += "G" + str(comment_counter) + ". " + goals.user_comments + "| "
            goals_manager_comments += "G" + str(comment_counter) + ". " + goals.manager_comments + "| "
            goals_board_comments += "G" + str(comment_counter) + ". " + goals.board_comments + "| "
        comment_counter=0
        
        for competencies in user_appraisal.competencies_set.all():
            comment_counter += 1
            competencies_employees_comments += "C" + str(comment_counter) + ". " + competencies.user_comments + "| "
            competencies_manager_comments += "C" + str(comment_counter) + ". " + competencies.manager_comments + "| "
            competencies_board_comments += "C" + str(comment_counter) + ". " + competencies.board_comments + "| "
        comment_counter=0

        for skills in user_appraisal.skills_set.all():
            comment_counter += 1
            skills_employees_comments += "S" + str(comment_counter) + ". " + skills.user_comments + "| "
            skills_manager_comments += "S" + str(comment_counter) + ". " + skills.manager_comments + "| "
            skills_board_comments += "S" + str(comment_counter) + ". " + skills.board_comments + "| "

            all_employees_TDR += "S" + str(comment_counter) + ". " + skills.recommended_Trainings_user + "| "
            all_managers_TDR += "S" + str(comment_counter) + ". " + skills.recommended_Trainings_manager + "| "
            all_board_TDR += "S" + str(comment_counter) + ". " + skills.recommended_Trainings_board + "| "
        comment_counter=0

        writer.writerow([name, department, job_title, manager_name, goals_count, competencies_count, skills_count, employee_rating, manager_rating, board_rating, all_employees_TDR, all_managers_TDR, all_board_TDR, goals_employees_comments, goals_manager_comments, goals_board_comments, competencies_employees_comments, competencies_manager_comments, competencies_board_comments, skills_employees_comments, skills_manager_comments, skills_board_comments,])
        
    response['Content-Disposition'] = 'attachment; filename="Training_Recommendation_Report.csv"'
    return response

@login_required(login_url='login')
def Comp_CalibrationReport(request, *args, **kwargs):
    context={}
    return render(request, 'Appraisals/Report_CompanyCR.html', context)
