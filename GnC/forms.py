from django.forms import Textarea, DateTimeField, DateField
from django import forms
from .models import Goals, Departmental_Goals, Competencies, KPI, Departmental_Competencies
from bootstrap_modal_forms.forms import BSModalModelForm

class CreateGoalsForm(forms.ModelForm): #class CreateGoalsForm(forms.ModelForm):
    metrics_evidence = forms.ImageField()
    class Meta: 
        model = Goals
        fields=['goal_category', 'summary', 'description', 'metrics_Used', 'weightage', 'due', 'metrics_evidence']
        labels = {
            "summary": "Goal Title",
            "goal_category": "Goal Category",
            "description": "Objective",
            "metrics_Used": "Tracking Source/Documents",
            "weightage": "Weightage (%)",
            "due": "Due (DD/MM/YYYY)",
            'metrics_evidence': 'Upload File'
        }
        widgets = {
            'goal_category': forms.Select(
                attrs={
                'class': 'form-control',
                }),
            'summary': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Goal Description',
                    'style': 'max-height:150px;'
                }),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter description of goal',
                    'style': 'max-height: 150px; resize: none'
                }),
            'metrics_Used': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Goal Description',
                    'style': 'max-height:150px;'
                }),
            'weightage': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter the weightage of this goal',   
                    'style': 'width: 50%' 
                }),
            'due': forms.DateTimeInput(
                attrs={'class': 'form-control datetimepicker-input',
                        'data-target': '#datetimepicker1',
                        'style': 'width: 50%'},  
                        format='%d/%m/%Y'),
            }
    def __init__(self, *args, **kwargs):
        super(CreateGoalsForm, self).__init__(*args, **kwargs)
        self.fields['metrics_evidence'].required = False


class UploadGoalsEvidence(forms.ModelForm): #class CreateGoalsForm(forms.ModelForm):
    metrics_evidence = forms.ImageField()
    class Meta: 
        model = Goals
        fields=['metrics_evidence']
        labels = {
            'metrics_evidence': 'Evidence'
        }
    def __init__(self, *args, **kwargs):
        super(UploadGoalsEvidence, self).__init__(*args, **kwargs)
        self.fields['metrics_evidence'].required = False

class CreateCompetenciesForm(forms.ModelForm):
    class Meta:
        model = Competencies
        fields=['competency_category', 'summary', 'description', 'weightage']
        labels = {
            "competency_category": "Core Values Competency Category",
            "summary": "Core Values Competency",
            "weightage": "Weightage (%)",
        }

        widgets = {
            'summary': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter a short summary of compentency'
                }),
            'competency_category': forms.Select(
                attrs={
                    'class': 'form-control'
                }),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter description of competency',
                    'style': 'max-height: 150px; resize: none'
                    }),

            'weightage': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter the weightage of this competency',  
                    'style': 'width: 50%'
                }),
            }

class CreateKPIsForm(forms.ModelForm):

    class Meta:
        model = KPI
        fields=['description', 'due']
        labels = {
            'description': 'KPI Title',
            "due": "Due (DD/MM/YYYY)",
        }
        widgets = {
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter description of KPI',
                    'style': 'max-height: 150px; resize: none'
            }),
            'due': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'},  format='%d/%m/%Y'),
            }

class UpdateKPIsForm(forms.ModelForm):

    class Meta:
        model = KPI
        fields=['description', 'due', 'progress']
        labels = {
            'description': 'KPI Title',
            "due": "Due (DD/MM/YYYY)",
            'progress': "Status"
        }
        widgets = {
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter description of KPI',
                    'style': 'max-height: 150px; resize: none'
            }),
            'due': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'},  format='%d/%m/%Y'),
            'appraisal': forms.Select(attrs={
                'class': 'form-control'
            }),
            }


class CreateDepartmentalGoalsForm(forms.ModelForm):

    #due = DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = Departmental_Goals
        fields=['summary', 'goal_category', 'description', 'due']
        labels = {
            "summary": "Goal Title",
            "description": "Objective",
            "goal_category": "Goal Category",
            "due": "Due (DD/MM/YYYY)"
        }
        widgets = {
            'department': forms.Select(attrs={
                'class': 'form-control'
            }),
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
            'due': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'style': 'width: 50%',
                'data-target': '#datetimepicker1'
            },  format='%d/%m/%Y'),
            }

class CreateDepartmentalCompetenciesForm(forms.ModelForm):
    class Meta:
        model = Departmental_Competencies
        fields=['competency_category', 'summary','description', ]
        labels = {
            "competency_category": "Competency Category",
            "summary": "Core Values Competency"
        }
        widgets = {
            'department': forms.Select(attrs={
                'class': 'form-control'
            }),
            'summary': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'competency_category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            })
            }

class UpdatePOSTKPIsForm(forms.ModelForm):
    class Meta:
        model = KPI
        fields=['progress']
        widgets = {
            'progress': forms.Select(attrs={'class': 'form-control'})
            }

class GoalsForm(forms.ModelForm):
    due = DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = Goals 
        fields= '__all__'
        labels = {
            "summary": "Objective",
            "weightage": "Weightage (%)"
        }
        widgets = {
            'appraisal': forms.Select(attrs={
                'class': 'form-control'
            }),
            'employee': forms.Select(attrs={
                'class': 'form-control'
            }),
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
            'due': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1'
            },  format='%d/%m/%Y'),
            
            'user_rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'manager_rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'board_rating': forms.Select(attrs={
                'class': 'form-control'
            })
            }


class DepartmentGoalsForm(forms.ModelForm):

    due = DateTimeField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = Departmental_Goals
        fields= '__all__'
        labels = {
            "summary": "Goal Title",
            "description": "Objective"
        }
        widgets = {
            'manager': forms.Select(attrs={
                'class': 'form-control'
            }),
            'appraisal': forms.Select(attrs={
                'class': 'form-control'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control'
            }),
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
            'due': forms.DateInput(attrs={
                'class': 'form-control'
            })
        
         }
        

class CompetenciesForm(forms.ModelForm):
    class Meta:
        model = Competencies
        fields= '__all__'
        labels = {
            "summary": "Description"
        }
        widgets = {
            'manager': forms.Select(attrs={
                'class': 'form-control'
            }),
            'appraisal': forms.Select(attrs={
                'class': 'form-control'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control'
            }),
            'summary': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'competency_category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-height: 150px; resize: none'
            })
        }

    
