from .models import Trainings, Apply_Trainings, Survey_Trainings, Skills, skill_category, Training_Courses
from .forms import CreateSkillsForm, CreateskillcategoryForm
from Appraisals.models import User_Appraisal_List

from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import Group, User


@method_decorator(login_required(login_url='login'), name='dispatch')
class Create_Skills(CreateView):
    form_class = CreateSkillsForm
    success_url = reverse_lazy('user_homepage')
    template_name = 'Trainings/HuNet_CreateSkills.html'

    def form_valid(self, form):
        id = self.kwargs.get("pk")
        user_appraisal_list = User_Appraisal_List.objects.get(id=id)

        form.instance.appraisal = user_appraisal_list
        form.instance.employee = self.request.user.profile

        print(form.cleaned_data)
        return super(Create_Skills, self).form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class Create_skill_category(CreateView):
    form_class = CreateskillcategoryForm
    success_url = reverse_lazy('user_homepage')
    template_name = 'Trainings/HuNet_Createskillcat.html'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(Create_skill_category, self).form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class Update_Skills(UpdateView):
    model = Skills
    form_class = CreateSkillsForm
    success_url = reverse_lazy('user_homepage')
    template_name = 'Trainings/HuNet_UpdateSkills.html'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(Update_Skills, self).form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class Skills_Delete(DeleteView):
    model = Skills
    template_name = 'Trainings/HuNet_DeleteSkills.html'
    success_url = reverse_lazy('user_homepage')

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Skills, id=id)


@login_required(login_url='login')
def hyperlink_training_courses(request, *args, **kwargs):
    all_training_courses_database = Training_Courses.objects.all()
    if request.method == 'GET':
        skill_name = request.GET.get('search')
        if skill_name == ' ' or skill_name == '':
            pass
        try:
            filtered_training_database = Training_Courses.objects.filter(skill_category__name__icontains=skill_name)
            return render(request, 'Trainings/Hyperlink_TrainingList.html',
                          {'training_course_list': filtered_training_database})
        except:
            pass

    context = {
        'training_course_list': all_training_courses_database
    }
    return render(request, 'Trainings/Hyperlink_TrainingList.html', context)
