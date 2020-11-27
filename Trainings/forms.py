from django.forms import Textarea 
from django import forms
from .models import Skills, skill_category

class CreateSkillsForm(forms.ModelForm):
    class Meta: 
        model = Skills
        fields=['skill_category', 'description', 'weightage']
        labels = {
            "description": "Skill",
            "weightage": "Weightage (%)",
            "skill_category": "Skill Category" 
        }
        widgets = { 
            'skill_category': forms.Select(
                attrs={
                'class': 'form-control',
                }),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter description of skill',
                    'style': 'max-height: 150px; resize: none'
                }),
            'weightage': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter the weightage of this skill',
                    'style': 'width: 50%'
                }),
            }

class CreateskillcategoryForm(forms.ModelForm):
    class Meta: 
        model = skill_category
        fields=['name']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter name of skill'
                }),
            }
