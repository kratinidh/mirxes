from django import forms
from django.forms import Textarea, DateTimeField, DateField
from .models import peerAppraisal, peerAppraisalQuestion, Appraisal_Category, Overall_Appraisal, Rating_Scale
from GnC.models import Goals, Competencies
from Trainings.models import Skills,Career_Discussion
from Appraisals.models import User_Appraisal_List
from bootstrap_modal_forms.forms import BSModalModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Row, Submit, Button, Column

#from .models import Appraisal
#from django.forms.models import inlineformset_factory
#
#class CreateAppraisalForm(forms.ModelForm):
#    class Meta:
#        model = Appraisal
#        fields=[
#            'employee_list',
#            'user',
#            'manager',
#            'status',
#            'created_by',
#            'rating_scale'
#        ]
#
#GoalsFormset= inlineformset_factory(Appraisal, Goals)
#CompetenciesFormset= inlineformset_factory(Appraisal, #Competencies)

#Appraisals/HuNet_Update.html

class CreateAppraisalCategoryForm(forms.ModelForm):
    class Meta:
        model = Appraisal_Category
        fields = [
            'name',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CreateOverallAppraisalForm_Stage1(forms.ModelForm): 
    
    class Meta:
        model = Overall_Appraisal
        fields = (
            'name',
            'appraisal_category',
        )     
        labels = {
            "name": "Performance Appraisal",
            "appraisal_category": "Appraisal Category"
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'appraisal_category': forms.Select(attrs={'class': 'form-control'}),
        }

class CreateOverallAppraisalForm_Stage3(forms.ModelForm): 
    start_date = DateField(input_formats=['%d/%m/%Y']),

    mid_year_end_date = DateField(input_formats=['%d/%m/%Y']),

    goals_setting_end_date = DateField(input_formats=['%d/%m/%Y']),

    appraisal_end_date = DateField(input_formats=['%d/%m/%Y']),

    reports_end_date = DateField(input_formats=['%d/%m/%Y']),


    class Meta:
        model = Overall_Appraisal
        fields = (
            'start_date',
            'goals_setting_end_date',
            'mid_year_start_date',
            'mid_year_end_date',
            'end_year_start_date',
            'appraisal_end_date',
            'reports_end_date',
            'calibration_end_date',
        )     
        labels = {
            'start_date': 'Start Date',
            'goals_setting_end_date': 'Goals Setting End Date',
            'mid_year_start_date': 'Mid-Year Review Start Date',
            'mid_year_end_date': 'Mid-Year Review End Date',
            'end_year_start_date': 'Year-End Review Start Date',
            'appraisal_end_date': 'Year-End Appraisal End Date',
            "reports_end_date": "Moderation By Management End Date (DD/MM/YYYY)",
            "calibration_end_date": "Calibration End Date (DD/MM/YYYY)"
        }
        widgets = {
            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',
                'style': 'width: 50%'},  format='%d/%m/%Y'),
            
            'goals_setting_end_date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',  
                'style': 'width: 50%'}, format='%d/%m/%Y'),

            'mid_year_start_date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',
                'style': 'width: 50%'},  format='%d/%m/%Y'),

            'mid_year_end_date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',  
                'style': 'width: 50%'}, format='%d/%m/%Y'),

            'end_year_start_date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',  
                'style': 'width: 50%'}, format='%d/%m/%Y'),

            'appraisal_end_date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',
                'style': 'width: 50%'},  format='%d/%m/%Y'),

            'reports_end_date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',
                'style': 'width: 50%'},  format='%d/%m/%Y'),

            'calibration_end_date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',
                'style': 'width: 50%'},  format='%d/%m/%Y'),
        }

class CreateOverallAppraisalForm_Stage4(forms.ModelForm): 
    class Meta:
        model = Overall_Appraisal
        fields = (
            'goal_weightage',
            'competency_weightage',
            'skill_weightage',
        )     
        labels = {
            "goal_weightage": "Goal Weightage (%)",
            "competency_weightage": "Core Values Competency Weightage (%)",
            "skill_weightage": "Skill Weightage (%)"
        }

        widgets = {
            'goal_weightage': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter weightage of Goals',
                    'style': 'width: 70%'  
                }),
            'competency_weightage': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter weightage of Core Values Competency',
                    'style': 'width: 70%'   
                }),
            'skill_weightage': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter weightage of Skills',
                    'style': 'width: 70%'     
                }),
        }

class UpdateOverallAppraisalForm(forms.ModelForm): 

    start_date = DateField(input_formats=['%d/%m/%Y']),

    goals_setting_end_date = DateField(input_formats=['%d/%m/%Y']),

    mid_year_end_date = DateField(input_formats=['%d/%m/%Y']),

    appraisal_end_date = DateField(input_formats=['%d/%m/%Y']),

    reports_end_date = DateField(input_formats=['%d/%m/%Y']),

    #calibration_end_date = DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = Overall_Appraisal
        fields = (
            'status',

            'start_date',
            'goals_setting_end_date',
            'mid_year_start_date',
            'mid_year_end_date',
            'end_year_start_date',
            'appraisal_end_date',
            'reports_end_date',
            'calibration_end_date',
            
            'goal_weightage',
            'competency_weightage',
            'skill_weightage',
        )     
        labels = {
            "start_date": "Start Date (DD/MM/YYYY)",
            "goals_setting_end_date": "Goals Setting End Date (DD/MM/YYYY)",
            "mid_year_end_date": "Mid-Year Reviews End Date (DD/MM/YYYY)",
            "appraisal_end_date": "Year-End Appraisal End Date (DD/MM/YYYY)",
            "reports_end_date": "Moderation By Management End Date (DD/MM/YYYY)",
            "calibration_end_date": "Calibration End Date (DD/MM/YYYY)",

            "goal_weightage": "Goal Weightage (%)",
            "competency_weightage": "Core Values Competency Weightage (%)",
            "skill_weightage": "Skill Weightage (%)",
        }
        widgets = {
            
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),

            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',
                'style': 'width: 50%'},  format='%d/%m/%Y'),
            
            'goals_setting_end_date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',
                'style': 'width: 50%'},  format='%d/%m/%Y'),

            'mid_year_start_date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',
                'style': 'width: 50%'},  format='%d/%m/%Y'),

            'mid_year_end_date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',
                'style': 'width: 50%'},  format='%d/%m/%Y'),

            'end_year_start_date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',
                'style': 'width: 50%'},  format='%d/%m/%Y'),

            'appraisal_end_date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',
                'style': 'width: 50%'},  format='%d/%m/%Y'),

            'reports_end_date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',
                'style': 'width: 50%'},  format='%d/%m/%Y'),

            'calibration_end_date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',
                'style': 'width: 50%'},  format='%d/%m/%Y'),

            'goal_weightage': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter the weightage of Goals',
                    'style': 'width: 50%'    
                }),
            'competency_weightage': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter the weightage of Core Values Competency',
                    'style': 'width: 50%'    
                }),
            'skill_weightage': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter the weightage of Skills',
                    'style': 'width: 50%'    
                })
        }

class CreateOverallAppraisalForm_Ref(forms.ModelForm): 

    start_date = DateField(input_formats=['%d/%m/%Y']),

    goals_setting_end_date = DateField(input_formats=['%d/%m/%Y']),

    appraisal_end_date = DateField(input_formats=['%d/%m/%Y']),

    reports_end_date = DateField(input_formats=['%d/%m/%Y']),

    calibration_end_date = DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = Overall_Appraisal
        fields = (
            'name',
            'appraisal_category',
            'goal_weightage',
            'competency_weightage',
            'skill_weightage',
            'start_date',
            'goals_setting_end_date',
            'appraisal_end_date',
            'reports_end_date',
            'calibration_end_date',
            'status'
        )     
        labels = {
            "goal_weightage": "Goal Weightage(%)",
            "competency_weightage": "Competency Weightage(%)",
            "skill_weightage": "Skill Weightage(%)",

            "start_date": "Start Date (DD/MM/YYYY)",
            "goals_setting_end_date": "Goals Setting End Date (DD/MM/YYYY)",
            "appraisal_end_date": "Year-End Appraisal End Date (DD/MM/YYYY)",
            "reports_end_date": "Moderation By Management End Date (DD/MM/YYYY)",
            "calibration_end_date": "Calibration End Date (DD/MM/YYYY)"
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'appraisal_category': forms.Select(attrs={'class': 'form-control'}),

            'goal_weightage': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter the weightage of Goals'    
                }),
            'competency_weightage': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter the weightage of Core Values Competency'    
                }),
            'skill_weightage': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter the weightage of Skills'    
                }),
            
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'},  format='%d/%m/%Y'),
            
            'goals_setting_end_date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'},  format='%d/%m/%Y'),

            'appraisal_end_date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'},  format='%d/%m/%Y'),

            'reports_end_date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'},  format='%d/%m/%Y'),

            'calibration_end_date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'},  format='%d/%m/%Y'),

            'status': forms.Select(attrs={'class': 'form-control'})
        }

class CreateCareerDiscussionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
       super(CreateCareerDiscussionForm, self).__init__(*args, **kwargs)
       self.fields['Q1'].widget.attrs['readonly'] = True
       self.fields['Q2'].widget.attrs['readonly'] = True
       self.fields['Q3'].widget.attrs['readonly'] = True
       self.fields['Q4'].widget.attrs['readonly'] = True
    class Meta:
        model = Career_Discussion
        fields = (
            'Q1',
            'Q2',
            'Q3',
            'Q4',
            'Q5',
        )
        labels = {
            "Q1": "Where do I want to be in the next 1-3 years?",
            "Q2": "What are my strengths?",
            "Q3": "What are the areas I should develop?",
            "Q4": "What are some of the development activities?",
            "Q5": "Supervisor's comments?",
        }
        widgets = {
            'Q1': forms.Textarea(
                attrs={'class': 'form-control col-8',
                        'style': 'font-size: 16px; height: 120px; resize: none;'
                }),
            'Q2': forms.Textarea(
                attrs={'class': 'form-control col-8',
                        'style': 'font-size: 16px; height: 120px; resize: none;'
                }),
            'Q3': forms.Textarea(
                attrs={'class': 'form-control col-8',
                        'style': 'font-size: 16px; height: 120px; resize: none'
                }),
            'Q4': forms.Textarea(
                attrs={'class': 'form-control col-8',
                        'style': 'font-size: 16px; height: 120px; resize: none'
                }),
            'Q5': forms.Textarea(
                attrs={'class': 'form-control col-8',
                        'style': 'font-size: 16px; height: 120px; resize: none'
                }),
        }

class CreateCareerDiscussionForm2(forms.ModelForm):
    class Meta:
        model = Career_Discussion
        fields = (
            'Q1',
            'Q2',
            'Q3',
            'Q4',
        )
        labels = {
            "Q1": "Where do I want to be in the next 1-3 years?",
            "Q2": "What are my strengths?",
            "Q3": "What are the areas I should develop?",
            "Q4": "What are some of the development activities?",
        }
        widgets = {
            'Q1': forms.Textarea(
                attrs={'class': 'form-control col-8',
                        'style': 'font-size: 16px; height: 120px; resize: none;'
                }),
            'Q2': forms.Textarea(
                attrs={'class': 'form-control col-8',
                        'style': 'font-size: 16px; height: 120px; resize: none;'
                }),
            'Q3': forms.Textarea(
                attrs={'class': 'form-control col-8',
                        'style': 'font-size: 16px; height: 120px; resize: none'
                }),
            'Q4': forms.Textarea(
                attrs={'class': 'form-control col-8',
                        'style': 'font-size: 16px; height: 120px; resize: none'
                })
        }

class CreateRatingScaleForm(forms.ModelForm):
    class Meta:
        model = Rating_Scale
        fields = (
            'name',
            'description',
            'limiter'
        )     
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'limiter': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

class MidAppGoalsForm(forms.ModelForm):
    tracking_status = forms.ChoiceField(choices=(('On Track', 'On Track'),
    ('Not On Track', 'Not On Track')))
    
    def __init__(self, *args, **kwargs):
       super(MidAppGoalsForm, self).__init__(*args, **kwargs)
       self.fields['summary'].widget.attrs['readonly'] = True
       self.fields['goal_category'].widget.attrs['readonly'] = True
       self.fields['description'].widget.attrs['readonly'] = True
    class Meta:
        model = Goals
        fields = (
            'summary',
            'goal_category',
            'description',
            'tracking_status',
            'MID_user_comments',
            'id'
        )
        labels = {
            "summary": "Goal Title",
            "goal_category": "Goal Category",
            "description": "Objectives",
            "tracking_status": "Status",
            "MID_user_comments": "Employee's Comments",

        }
        widgets = {
            'summary': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'goal_category': forms.Select(attrs={
                'class': 'form-control' 
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'tracking_status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'MID_user_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 50px; resize: none'
            }),
        }

class MidAppGoalsForm_M(forms.ModelForm):
    tracking_status = forms.ChoiceField(choices=(('On Track', 'On Track'),
    ('Not On Track', 'Not On Track')))
    
    def __init__(self, *args, **kwargs):
       super(MidAppGoalsForm_M, self).__init__(*args, **kwargs)
       self.fields['summary'].widget.attrs['readonly'] = True
       self.fields['goal_category'].widget.attrs['readonly'] = True
       self.fields['description'].widget.attrs['readonly'] = True
       self.fields['tracking_status'].widget.attrs['readonly'] = True
       self.fields['MID_user_comments'].widget.attrs['readonly'] = True

    class Meta:
        model = Goals
        fields = (
            'summary',
            'goal_category',
            'description',
            'tracking_status',
            'MID_user_comments',
            'MID_manager_comments',
            'id'
        )
        labels = {
            "summary": "Goal Title",
            "goal_category": "Goal Category",
            "description": "Objectives",
            "tracking_status": "Status",
            "MID_user_comments": "Employee's Comments",
            "MID_manager_comments": "Manager's Comment",
        }

        widgets = {
            'summary': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'goal_category': forms.Select(attrs={
                'class': 'form-control' 
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'tracking_status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'MID_user_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 50px; resize: none'
            }),
            'MID_manager_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 50px; resize: none'
            }),
        }

class AppGoalsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
       super(AppGoalsForm, self).__init__(*args, **kwargs)
       self.fields['summary'].widget.attrs['readonly'] = True
       self.fields['goal_category'].widget.attrs['readonly'] = True
       self.fields['description'].widget.attrs['readonly'] = True

    class Meta:
        model = Goals
        fields = (
            'summary',
            'goal_category',
            'description',
            'user_rating',
            'user_comments',
            'id'
        )

        labels = {
            "summary": "Goal Title",
            "goal_category": "Goal Category",
            "description": "Objective",
            "user_rating": "Employee's Rating",
            "user_comments": "Employee's Comments",
        }
        
        widgets = {
            'summary': forms.TextInput(
                attrs={'class': 'form-control',
                        'style': 'width: 60%; font-size: 16px;'
                }),

            'goal_category': forms.Select(
                attrs={'class': 'form-control',
                        'style': 'width: 60%; font-size: 16px;'
                }),

            'description': forms.Textarea(
                attrs={'class': 'form-control',
                        'style': 'height: 120px; width: 60%; font-size: 16px; resize: none',
                }),

            'user_rating': forms.Select(
                attrs={'class': 'form-control',
                        'style': 'width: 60%; font-size: 16px;'
                }),

            'user_comments': forms.Textarea(
                attrs={'class': 'form-control',
                        'style':'width: 60%; height: 120px; font-size: 16px;'
                }),
        }


class AppCompetenciesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
       super(AppCompetenciesForm, self).__init__(*args, **kwargs)
       self.fields['summary'].widget.attrs['readonly'] = True
       self.fields['competency_category'].widget.attrs['readonly'] = True
       self.fields['description'].widget.attrs['readonly'] = True

    class Meta:
        model = Competencies
        fields = (
            'summary',
            'competency_category',
            'description',
            'user_rating',
            'user_comments',
            'id'
        )

        labels = {
            "summary": "Core Values Competency",
            'competency_category': "Competency Category",
            "user_rating": "Employee's Rating",
            "user_comments": "Employee's Comments",
        }


        widgets = {
            'summary': forms.TextInput(
                attrs={'class': 'form-control',
                'style': 'width: 50%; font-size: 16px;'
                }),
            'competency_category': forms.Select(
                attrs={'class': 'form-control',
                'style': 'width: 50%; font-size: 16px;'
                }),
            'description': forms.Textarea(
                attrs={'class': 'form-control',
                'style': 'height: 120px; width: 50%; font-size: 16px; resize: none'
                }),
            'user_rating': forms.Select(
                attrs={'class': 'form-control',
                'style': 'width: 50%; font-size: 16px;'
                }),
            'user_comments': forms.Textarea(
                attrs={'class': 'form-control',
                'style': 'height: 120px; width: 50%; font-size: 16px; resize: none'}),
        } 

class AppSkillsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
       super(AppSkillsForm, self).__init__(*args, **kwargs)
       self.fields['description'].widget.attrs['readonly'] = True
       self.fields['skill_category'].widget.attrs['readonly'] = True
    class Meta:
        model = Skills
        fields = (
            'skill_category',
            'description',
            'user_rating',
            'user_comments',
            'recommended_Trainings_user',
            'id'
        )

        labels = {
            "description": "Skill",
            'skill_category': "Skill Category",
            "user_rating": "Employee's Rating",
            "user_comments": "Employee's Comments",
            "recommended_Trainings_user": "Recommended Trainings"
        }

        widgets = {
            'skill_category': forms.Select(
                attrs={'class': 'form-control',
                'style': 'width: 50%; font-size: 16px;'}),

            'description': forms.Textarea(
                attrs={'class': 'form-control',
                'style': 'height: 120px; width: 50%; font-size: 16px; resize: none'
                }),

            'user_rating': forms.Select(
                attrs={'class': 'form-control',
                'style': 'width: 50%; font-size: 16px;'
                }),

            'user_comments': forms.Textarea(
                attrs={'class': 'form-control',
                'style': 'height: 120px; width: 50%; font-size: 16px; resize: none'
                }),

            'recommended_Trainings_user': forms.Textarea(
                attrs={'class': 'form-control',
                'style': 'height: 120px; width: 50%; font-size: 16px; resize: none'
                }),
        } 

class peerAppraisalForm(forms.ModelForm):
    class Meta:
        model = peerAppraisal
        fields = '__all__'

#Appraisals/HuNet_UpdateG.html
class MAppGoalsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
       super(MAppGoalsForm, self).__init__(*args, **kwargs)
       self.fields['summary'].widget.attrs['readonly'] = True
       self.fields['goal_category'].widget.attrs['readonly'] = True
       self.fields['description'].widget.attrs['readonly'] = True
       self.fields['user_rating'].widget.attrs['readonly'] = True
       self.fields['user_comments'].widget.attrs['readonly'] = True
    class Meta:
        model = Goals
        fields = (
            'summary',
            'goal_category',
            'description',
            'user_rating',
            'user_comments',
            'manager_rating',
            'manager_comments',
            'id'
        )

        labels = {
            "summary": "Goal Title",
            "description": "Objective",
            "user_rating": "Employee's Rating",
            "user_comments": "Employee's Comments", 
        }

        widgets = {
            'summary': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'goal_category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'user_rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'user_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'manager_rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'manager_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
        }

#Appraisals/HuNet_UpdateC.html
class MAppCompetenciesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
       super(MAppCompetenciesForm, self).__init__(*args, **kwargs)
       self.fields['summary'].widget.attrs['readonly'] = True
       self.fields['competency_category'].widget.attrs['readonly'] = True
       self.fields['description'].widget.attrs['readonly'] = True
       self.fields['user_rating'].widget.attrs['readonly'] = True
       self.fields['user_comments'].widget.attrs['readonly'] = True
    class Meta:
        model = Competencies
        fields = ( 
            'summary',
            'competency_category',
            'description',
            'user_rating',
            'user_comments',
            'manager_rating',
            'manager_comments',
            'id'
        )
        labels = {
            "summary": "Core Values Competency",
            "user_rating": "Employee's Rating",
            "user_comments": "Employee's Comments",
        }
        widgets = {
            'summary': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'competency_category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'user_rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'user_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'manager_rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'manager_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
        }

class MAppSkillsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
       super(MAppSkillsForm, self).__init__(*args, **kwargs)
       self.fields['skill_category'].widget.attrs['readonly'] = True
       self.fields['description'].widget.attrs['readonly'] = True
       self.fields['user_rating'].widget.attrs['readonly'] = True
       self.fields['user_comments'].widget.attrs['readonly'] = True
       self.fields['recommended_Trainings_user'].widget.attrs['readonly'] = True
    class Meta:
        model = Skills
        fields = (
            'skill_category',
            'description',
            'user_rating',
            'user_comments',
            'recommended_Trainings_user',
            'manager_rating',
            'manager_comments',
            'recommended_Trainings_manager',
            'id'
        )
        labels = {
            "description": "Skill",
            "user_rating": "Employee's Rating",
            "user_comments": "Employee's Comments",
            "recommended_Trainings_user": "Recommended Trainings",
            "recommended_Trainings_manager": "Recommended Trainings"
        }
        widgets = {
            'skill_category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'user_rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'user_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'recommended_Trainings_user': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'manager_rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'manager_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'recommended_Trainings_manager': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
        }


#Appraisals/HuNet_UpdateG.html
class BAppGoalsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
       super(BAppGoalsForm, self).__init__(*args, **kwargs)
       self.fields['summary'].widget.attrs['readonly'] = True
       self.fields['goal_category'].widget.attrs['readonly'] = True
       self.fields['description'].widget.attrs['readonly'] = True
       self.fields['user_rating'].widget.attrs['readonly'] = True
       self.fields['user_comments'].widget.attrs['readonly'] = True
       self.fields['manager_rating'].widget.attrs['readonly'] = True
       self.fields['manager_comments'].widget.attrs['readonly'] = True

    class Meta:
        model = Goals
        fields = (
            'summary',
            'goal_category',
            'description',
            'user_rating',
            'user_comments',
            'manager_rating',
            'manager_comments',
            'board_rating',
            'board_comments',
            'id'
        )

        labels = {
            "summary": "Goal Title",
            "description": "Objective",
            "user_rating": "Employee's Rating",
            "user_comments": "Employee's Comments",
        }

        widgets = {
            'summary': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'goal_category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'user_rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'user_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'manager_rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'manager_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'board_rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'board_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
        }

#Appraisals/HuNet_UpdateC.html
class BAppCompetenciesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
       super(BAppCompetenciesForm, self).__init__(*args, **kwargs)
       self.fields['summary'].widget.attrs['readonly'] = True
       self.fields['competency_category'].widget.attrs['readonly'] = True
       self.fields['description'].widget.attrs['readonly'] = True
       self.fields['user_rating'].widget.attrs['readonly'] = True
       self.fields['user_comments'].widget.attrs['readonly'] = True
       self.fields['manager_rating'].widget.attrs['readonly'] = True
       self.fields['manager_comments'].widget.attrs['readonly'] = True

    class Meta:
        model = Competencies
        fields = ( 
            'summary',
            'competency_category',
            'description',
            'user_rating',
            'user_comments',
            'manager_rating',
            'manager_comments',
            'board_rating',
            'board_comments',
            'id'
        )
        labels = {
            "summary": "Core Values Competency",
            "user_rating": "Employee's Rating",
            "user_comments": "Employee's Comments"
        }
        widgets = {
            'summary': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'competency_category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'user_rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'user_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'manager_rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'manager_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'board_rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'board_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
        }

class BAppSkillsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
       super(BAppSkillsForm, self).__init__(*args, **kwargs)
       self.fields['skill_category'].widget.attrs['readonly'] = True
       self.fields['description'].widget.attrs['readonly'] = True
       self.fields['user_rating'].widget.attrs['readonly'] = True
       self.fields['user_comments'].widget.attrs['readonly'] = True
       self.fields['recommended_Trainings_user'].widget.attrs['readonly'] = True
       self.fields['manager_rating'].widget.attrs['readonly'] = True
       self.fields['manager_comments'].widget.attrs['readonly'] = True
       self.fields['recommended_Trainings_manager'].widget.attrs['readonly'] = True
    class Meta:
        model = Skills
        fields = (
            'skill_category',
            'description',
            'user_rating',
            'user_comments',
            'recommended_Trainings_user',
            'manager_rating',
            'manager_comments',
            'recommended_Trainings_manager',
            'board_rating',
            'board_comments',
            'recommended_Trainings_board',
            'id'
        )
        labels = {
            "description": "Skill",
            "user_rating": "Employee's Rating",
            "user_comments": "Employee's Comments",
            "recommended_Trainings_user": "Recommended Trainings",
            "recommended_Trainings_manager": "Recommended Trainings",
            "recommended_Trainings_board": "Recommended Trainings",
            
        }
        widgets = {
            'skill_category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'user_rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'user_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'recommended_Trainings_user': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'manager_rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'manager_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'recommended_Trainings_manager': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'board_rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'board_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
            'recommended_Trainings_board': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
        }

class GoalsSettingRejectionForm(forms.ModelForm):
    class Meta:
        model = User_Appraisal_List
        fields = ('goals_settingM_rejection',)
        labels = {
            'goals_settingM_rejection': 'Comments:',
        }
        widgets = {
            'goals_settingM_rejection': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
        }

class MidYearRejectionForm(forms.ModelForm):
    class Meta:
        model = User_Appraisal_List
        fields = ('mid_yearM_rejection',)
        labels = {
            'mid_yearM_rejection': 'Comments:',
        }
        widgets = {
            'mid_yearM_rejection': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
        }

class AppraisalRejectionForm(forms.ModelForm):
    class Meta:
        model = User_Appraisal_List
        fields = ('appraisalHR_rejection',)
        labels = {
            'appraisalHR_rejection': 'Comments: ',
        }
        widgets = {
            'appraisalHR_rejection': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
        }

#Important
class TryingOutForm(forms.ModelForm):
    class Meta:
        model = User_Appraisal_List
        fields = ('employee',)

class BAppForm(forms.ModelForm):
    class Meta:
        model = User_Appraisal_List
        fields = (
            'overall_board_comments',
        )

        widgets: {
            'overall_board_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            }),
        }
#Appraisals/HuNet_UpdatepAQn.html

class CreatePeerAppraisalForm(forms.ModelForm):
    class Meta:
        model = peerAppraisal
        fields = (
            'appraisal',
            'viewer',
            'title1',
            'title2',
            'title3',      
            )
        widgets = {
            'appraisal': forms.Select(attrs={'class': 'form-control'}),

            'title1': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Question'    
                }),
            
            'title2': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Question'    
                }),
            
            'title3': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Question'    
                })
        }

class UpdatePeerAppraisalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
       super(UpdatePeerAppraisalForm, self).__init__(*args, **kwargs)
       self.fields['title1'].widget.attrs['readonly'] = True
       self.fields['title2'].widget.attrs['readonly'] = True
       self.fields['title3'].widget.attrs['readonly'] = True
    class Meta:
        model = peerAppraisal
        fields = (
            'title1',
            'strength1',
            'weaknessdevelopment1',
            'title2',
            'strength2',
            'weaknessdevelopment2',
            'title3',      
            'strength3',
            'weaknessdevelopment3',
            )
        widgets = {

            'title1': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Question'    
                }),
            'strength1': forms.Textarea(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Strength',
                    'style': 'height: 6em; resize: none' ,
   
                }),
            'weaknessdevelopment1': forms.Textarea(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Weakness/Area of Development',
                    'style': 'height: 6em; resize: none' ,
   
                }),
            
            'title2': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Question'    
                }),
            'strength2': forms.Textarea(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Strength',
                    'style': 'height: 6em; resize: none',
      
                }),
            'weaknessdevelopment2': forms.Textarea(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Weakness/Area of Development',
                    'style': 'height: 6em; resize: none',
    
                }),
            
            'title3': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Question'    
                }),
            'strength3': forms.Textarea(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Strength',
                    'style': 'height: 6em; resize: none',
   
                }),
            'weaknessdevelopment3': forms.Textarea(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Weakness/Area of Development',
                    'style': 'height: 6em; resize: none',
                           
                }),
        }

class UpdateUserAppRatingForm(forms.ModelForm): 
    class Meta:
        model = User_Appraisal_List
        fields = (
        )     

class UpdateManagerAppRatingForm(forms.ModelForm): 
    class Meta:
        model = User_Appraisal_List
        fields = (
            'incrementRecommendation',
            'bonusRecommendation'
        )     
        labels ={
            'incrementRecommendation': 'Increment Recommendation (%)',
            'bonusRecommendation': 'Bonus Recommendation (Fixed)'
        }
        widgets={
            'incrementRecommendation': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Increment Disembursement',
                    'style': 'width:40%'    
                    
                }),
            'bonusRecommendation': forms.Textarea(
                attrs={'class': 'form-control col-8',
                        'style': 'font-size: 16px; height: 120px; resize: none; width:40%;'
                }),
        }

class UpdateBoardAppRatingForm(forms.ModelForm): 
    class Meta:
        model = User_Appraisal_List
        fields = (
            'recommendationComments',
        )     
        labels ={
            'recommendationComments': 'Recommendation Comments',
        }
        widgets={
            'recommendationComments': forms.Textarea(
                attrs={'class': 'form-control col-8',
                        'style': 'font-size: 16px; height: 120px; resize: none;'
                }),
        }