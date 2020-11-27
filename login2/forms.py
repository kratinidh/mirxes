from django import forms
from django.forms import ModelForm
from Profile.models import Profile, Qualifications
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from phonenumber_field.formfields import PhoneNumberField

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
        }

class CreateProfileForm(forms.ModelForm):
    phone = PhoneNumberField(widget=forms.TextInput(attrs={
        'class': 'form-control', }))
                
    class Meta:
        model = Profile
        fields=[
            'name',
            'employee_ID',
            'nric',

            'typeOfEmployee',
            'email',
            'department',
            'gender',
            'address_1',
            'address_2',
            'date_Of_Passport_Expiry',
            'citizenship_Status',
            'job_Title',
            'date_Of_Hire',
            'employment_Type',
            'first_Reporting_Manager',
            'second_Reporting_Manager',
            'division_Centre',
            'phone',

            'skill1',
            'skill2',
            'skill3'
        ]
        labels = {
            'employee_ID': 'Employee Code',
            'nric': 'NRIC/FIN',
            'typeOfEmployee': 'Indirect/Direct',
            'email': 'Email',
            'department' : 'Department',
            'gender' : 'Gender',
            'address_1' : 'Home Address',
            'address_2' : 'Alternate Home Address',
            'date_Of_Passport_Expiry' : 'Passport Expiry Date',
            'citizenship_Status' : 'Citizenship Status',
            'job_Title' : 'Job Title',
            'employment Type' : 'Employment Type',
            'first_Reporting_Manager' : 'Direct Manager',
            'second_Reporting_Manager' : 'HOD',
            'division_Centre' : 'Section',
            'phone' : 'Phone (Add Country Code)',
            'skill1': 'Skill 1',
            'skill2': 'Skill 2',
            'skill3': 'Skill 3'
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Name'
                }),
            'employee_ID': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter ID'
                }),
            'nric': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter NRIC/FIN'
                }),
            'typeOfEmployee': forms.Select(
                attrs={
                    'class': 'form-control',
                }),
            'email': forms.EmailInput(attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Email'
                }),
            'department': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Select Department',
                }),
            'gender': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Select Gender',
                }),
            'address_1': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Address',
                    'style': 'height: 4em;'
                }),
            'address_2': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Alternate Address',
                    'style': 'height: 4em;'
                }),
            
            'date_Of_Passport_Expiry': forms.DateTimeInput(
                attrs={'class': 'form-control datetimepicker-input',
                        'data-target': '#datetimepicker1',
                        'style': 'width: 50%'},  
                        format='%d/%m/%Y'),
            'citizenship_Status': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter ID'
                }),
            'job_Title': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Job Title',
                }),
                
            'date_Of_Hire': forms.DateTimeInput(
                attrs={'class': 'form-control datetimepicker-input',
                        'data-target': '#datetimepicker1',
                        'style': 'width: 50%'},  
                        format='%d/%m/%Y'),

            'employment_Type': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Select Employment Type',
                }),
            'first_Reporting_Manager': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Select Manager',
                }),
            'second_Reporting_Manager': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Name of Indirect Manager',
                }),
            'division_Centre':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Section',
                }),

            'skill1':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Name',
                }),

            'skill2':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Name',
                }),

            'skill3':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Name',
                }),
        }


class UpdateProfileForm_All(forms.ModelForm):
    phone = PhoneNumberField(widget=forms.TextInput(attrs={
        'class': 'form-control', }))
                
    class Meta:
        model = Profile
        fields=[
            'citizenship_Status',
            'first_Reporting_Manager',
            'second_Reporting_Manager',
            'division_Centre',
            'phone',

            'skill1',
            'skill2',
            'skill3'
        ]
        labels = {
            'citizenship_Status' : 'Citizenship Status',
            'first_Reporting_Manager' : 'Direct Manager',
            'second_Reporting_Manager' : 'HOD',
            'division_Centre' : 'Section',
            'phone' : 'Phone (Add Country Code)',
            'skill1': 'Skill 1',
            'skill2': 'Skill 2',
            'skill3': 'Skill 3'
        }
        widgets = {
            'citizenship_Status': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter ID'
                }),
            'first_Reporting_Manager': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Select Manager',
                }),
            'second_Reporting_Manager': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Name of Indirect Manager',
                }),
            'division_Centre':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Section',
                }),

            'skill1':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Name',
                }),

            'skill2':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Name',
                }),

            'skill3':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Name',
                }),
        }

class CreateQualificationsForm(forms.ModelForm):
    class Meta:
        model = Qualifications
        fields = ['name', 'institution','graduation_year']

        labels = {
            'institution': 'Institution',
            'name': 'Qualification',
            'graduation_year': 'Year Of Graduation',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Name'
                }),
            'institution': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Institution Name'
                }),
            'graduation_year': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Enter Graduation Year'
                }),
        }