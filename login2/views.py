import csv, io
from random import randint

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
# Create your views here.
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView

from Appraisals.models import User_Appraisal_List, peerAppraisal, Overall_Appraisal
from GnC.models import Departmental_Goals, Departmental_Competencies
from Profile.models import Profile, Departments, Qualifications
from Trainings.models import Skills
from login2.decorators import unauthenticated_user, allowed_users, admin_only
from .forms import CreateUserForm, CreateProfileForm, CreateQualificationsForm, UpdateProfileForm_All


def PROFILE_CREATION_EMAIL(name, username, email, typeOfEmployee):
    email_string = "Dear " + name + ", \n\nYour Performance Management System account has been created. Please see the login details below to access the system: \n\nUsername:" + username + "\nEmail: " + email + "\nPassword: DenselightPassword1234" + "\nAccess: " + typeOfEmployee + "\n\nPlease do not hesitate to contact the HR Department if you have any questions. \nThank you."
    return email_string


def PROFILE_UPDATE_EMAIL(user_profile):
    email_string = "Dear HR personnels, \n\n" + user_profile.name + " has made a profile change in the system. \nPlease login to the system to review the changes. \n\nThank you."
    return email_string


@unauthenticated_user
def registerPage(request):
    # If user is logged in, they will be auto redirected to homepage
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # Save filled form
            user = form.save()

            # Get user name without gettingother attributes
            username = form.cleaned_data.get('username')

            # When creating a user, immediately push them to employee group
            group = Group.objects.get(name='Employee')
            # Create variable that contain group name 'employee'
            user.groups.add(group)  # Push user's form into employee group
            Profile.objects.create(
                user=user,
            )
            # If request successful, print 'Account created for'
            messages.success(request, 'Account created for ' + username)
            return redirect('login')

    context = {
        'form': form
    }
    return render(request, 'login2/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        # if user exists
        if user is not None:
            # if email == user.email:
            login(request, user)
            return redirect('register')
            # else:
            # messages.info(request,'Email is incorrect')
        # if user does not exist
        else:
            messages.info(request, 'Username OR Password is incorrect')

    context = {}
    return render(request, 'login2/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
@allowed_users(allowed_roles=['Employee'])
def user_dashboard(request):
    # Dashboard Rubrics
    # !Filter to get all Goals Setting OA of user:
    rubric_overall_appraisal_database1 = Overall_Appraisal.objects.distinct().filter(
        user_appraisal_list__employee=request.user.profile, status='Stage 1').count

    # !Filter to get all Mid Year Review OA of user:
    rubric_overall_appraisal_database2 = Overall_Appraisal.objects.filter(
        user_appraisal_list__employee=request.user.profile, status='Stage 1B').count

    # !Filter to get all End Year OA of user:
    rubric_overall_appraisal_database3 = Overall_Appraisal.objects.filter(
        Q(status='Stage 2') | Q(status='Stage 3') | Q(status='Stage 4'),
        user_appraisal_list__employee=request.user.profile, ).count

    # Dashboard Information
    # !Filtering to get all uncompleted UAL of users
    user_appraisal_database = User_Appraisal_List.objects.filter(employee=request.user.profile).exclude(
        overall_appraisal__status__contains='Completed')

    # !Filtering to get profile of user's manager
    user_manager_database = Profile.objects.get(user=request.user).first_Reporting_Manager

    # Peer appraisal:
    # !Filtering to get all UAL with same managers that are undergoing appraisal stage, excluding personal UALs
    user_appraisal_list_database = User_Appraisal_List.objects.filter(
        manager=request.user.profile.first_Reporting_Manager, overall_appraisal__status__contains='Stage 2').exclude(
        employee=request.user.profile)

    # !Filtering to get all peerAppraisals with viewers = user
    peer_appraisal_database = peerAppraisal.objects.filter(viewer=request.user.profile).order_by('-completion')

    # Records
    # !Filtering to get all UAL with completed OA of user
    records_user_appraisal_database = User_Appraisal_List.objects.filter(
        overall_appraisal__status__contains='Completed', employee=request.user.profile)

    context = {
        # Get all Goals Setting OA of user:
        "rubic1": rubric_overall_appraisal_database1,
        # Get all Mid Year OA of user:
        "rubic2": rubric_overall_appraisal_database2,
        # Get all End Year OA of user:
        "rubic3": rubric_overall_appraisal_database3,

        # !Get all UAL with same managers that are undergoing appraisal stage, excluding personal UALs
        "user_appraisal_list": user_appraisal_database,
        # !Get profile of user's manager
        "req_user_manager": user_manager_database,

        # !Get all UAL with same managers that are undergoing appraisal stage, excluding personal UALs
        "user_appraisal_list_database": user_appraisal_list_database,

        # Get all peerAppraisals with viewers = user
        "peer_appraisal_database": peer_appraisal_database,
        # Reports
        "records_UAL_database": records_user_appraisal_database
    }
    return render(request, 'login2/HuNet_Dashboard1.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Manager'])
def manager_dashboard(request):
    # Dashboard Rubrics
    # !Filter to get all Goals Setting OA of user:
    rubric_overall_appraisal_database1 = Overall_Appraisal.objects.distinct().filter(
        user_appraisal_list__employee=request.user.profile, status='Stage 1').count

    # !Filter to get all Mid Year Review OA of user:
    rubric_overall_appraisal_database2 = Overall_Appraisal.objects.filter(
        user_appraisal_list__employee=request.user.profile, status='Stage 1B').count

    # !Filter to get all End Year OA of user:
    rubric_overall_appraisal_database3 = Overall_Appraisal.objects.filter(
        Q(status='Stage 2') | Q(status='Stage 3') | Q(status='Stage 4'),
        user_appraisal_list__employee=request.user.profile, ).count

    # Dashboard user
    # !Filtering to get all uncompleted UAL of users
    user_appraisal_database = User_Appraisal_List.objects.filter(employee=request.user.profile).exclude(
        overall_appraisal__status__contains='Completed')

    # !Filtering to get profile of user's manager
    user_manager_database = Profile.objects.get(user=request.user).first_Reporting_Manager

    # Peer appraisal:
    # !Filtering to get all UAL with same managers that are undergoing appraisal stage, excluding personal UALs
    user_appraisal_list_database = User_Appraisal_List.objects.filter(
        manager=request.user.profile.first_Reporting_Manager, overall_appraisal__status__contains='Stage 2').exclude(
        employee=request.user.profile)

    # !Filtering to get all peerAppraisals with viewers = user
    peer_appraisal_database = peerAppraisal.objects.filter(viewer=request.user.profile).order_by('-completion')

    # Department:
    # !Filtering to get all profile where manager = user (Subordinates)
    subordinates_database = Profile.objects.filter(first_Reporting_Manager=request.user.profile)

    # !Filtering to get Overall Appraisals in Stage 1
    subordinate_GCS_appraisal_database = Overall_Appraisal.objects.filter(Q(status='Stage 1') | Q(status='Stage 2'))

    # Filtering to get all UAL with stage = 1 where manager = user (Subordinates)
    subordinate_GCS_list_database = User_Appraisal_List.objects.filter(overall_appraisal__status__contains='Stage 1',
                                                                       manager=request.user.profile)

    # Filtering to get all uncompleted UAL where manager = user (Subordinates)
    subordinate_midyear_list_database = User_Appraisal_List.objects.filter(
        overall_appraisal__status__contains='Stage 1B', manager=request.user.profile)

    # Filtering to get all UAL with stage = 2 where manager = user (Subordinates)
    subordinate_appraisal_list_database = User_Appraisal_List.objects.filter(
        overall_appraisal__status__contains='Stage 2', manager=request.user.profile)

    # Filtering to get all UAL with stage = 3 where manager = user (Subordinates)
    subordinate_reports_list_database = User_Appraisal_List.objects.filter(
        overall_appraisal__status__contains='Stage 3', manager=request.user.profile)

    # Filtering to get all UAL with stage = 4 where manager = user (Subordinates)
    subordinate_calibration_list_database = User_Appraisal_List.objects.filter(
        overall_appraisal__status__contains='Stage 4', manager=request.user.profile)

    # Filtering to get all subordinate uncompleted UAL
    subordinate_appraisal_system_database = User_Appraisal_List.objects.filter(manager=request.user.profile).order_by(
        'employee', 'overall_appraisal__status')

    # !Filtering to get all departmental goals with manager = user + excluding completed OA
    MCreated_DG_database = Departmental_Goals.objects.filter(manager=request.user.profile).exclude(
        appraisal__status__contains='Completed')
    # !Filtering to get all departmental competencies with manager = user + excluding completed OA
    MCreated_DC_database = Departmental_Competencies.objects.filter(manager=request.user.profile).exclude(
        appraisal__status__contains='Completed')
    # Reports
    records_user_appraisal_database = User_Appraisal_List.objects.filter(
        overall_appraisal__status__contains='Completed', employee=request.user.profile)

    context = {
        # Get all Goals Setting OA of user:
        "rubic1": rubric_overall_appraisal_database1,
        # Get all Mid Year OA of user:
        "rubic2": rubric_overall_appraisal_database2,
        # Get all End Year OA of user:
        "rubic3": rubric_overall_appraisal_database3,

        # !Get all UAL with same managers that are undergoing appraisal stage, excluding personal UALs
        "user_appraisal_list": user_appraisal_database,
        # !Get profile of user's manager
        "req_user_manager": user_manager_database,

        # !Get all UAL with same managers that are undergoing appraisal stage, excluding personal UALs
        "user_appraisal_list_database": user_appraisal_list_database,
        # Get all peerAppraisals with viewers = user
        "peer_appraisal_database": peer_appraisal_database,

        # !Get all profile where manager = user (Subordinates)
        "subordinate_database": subordinates_database,
        # !Get all Overall Appraisals
        "department_GCS_database": subordinate_GCS_appraisal_database,
        # Get all UAL with stage = 1 where manager = user (Subordinates)
        "subordinate_GCS_database": subordinate_GCS_list_database,
        # Get all uncompleted UAL where manager = user (Subordinates)
        "subordinate_midyear_database": subordinate_midyear_list_database,
        # Get all UAL with stage = 2 where manager = user (Subordinates)
        "department_appraisal_database": subordinate_appraisal_list_database,
        # Get all UAL with stage = 3 where manager = user (Subordinates)
        "department_reports_database": subordinate_reports_list_database,
        # Get all UAL with stage = 4 where manager = user (Subordinates)
        "department_calibration_database": subordinate_calibration_list_database,
        # !Get all subordinate UAL
        "department_entire_subUAL_database": subordinate_appraisal_system_database,
        # !Get all departmental goals with manager = user + excluding completed OA
        "mcreated_dg_database": MCreated_DG_database,
        # !Get all departmental competencies with manager = user + excluding completed OA
        "mcreated_dc_database": MCreated_DC_database,

        "records_UAL_database": records_user_appraisal_database

    }
    return render(request, 'login2/HuNetM_Dashboard2.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['HR'])
def HR_dashboard(request):
    # Dashboard Rubrics
    # !Filter to get all Goals Setting OA of user:
    rubric_overall_appraisal_database1 = Overall_Appraisal.objects.distinct().filter(
        user_appraisal_list__employee=request.user.profile, status='Stage 1').count

    # !Filter to get all Mid Year Review OA of user:
    rubric_overall_appraisal_database2 = Overall_Appraisal.objects.filter(
        user_appraisal_list__employee=request.user.profile, status='Stage 1B').count

    # !Filter to get all End Year OA of user:
    rubric_overall_appraisal_database3 = Overall_Appraisal.objects.filter(
        Q(status='Stage 2') | Q(status='Stage 3') | Q(status='Stage 4'),
        user_appraisal_list__employee=request.user.profile, ).count

    # Dashboard user
    # !Get all UAL with same managers that are undergoing appraisal stage, excluding personal UALs
    user_appraisal_database = User_Appraisal_List.objects.filter(employee=request.user.profile).exclude(
        overall_appraisal__status__contains='Completed')
    # !Get profile of user's manager
    user_manager_database = Profile.objects.get(user=request.user).first_Reporting_Manager

    # Peer appraisal:
    # !Filtering to get all UAL with same managers that are undergoing appraisal stage, excluding personal UALs
    user_appraisal_list_database = User_Appraisal_List.objects.filter(
        manager=request.user.profile.first_Reporting_Manager, overall_appraisal__status__contains='Stage 2').exclude(
        employee=request.user.profile)

    # !Filtering to get all peerAppraisals with viewers = user
    peer_appraisal_database = peerAppraisal.objects.filter(viewer=request.user.profile).order_by('-completion')

    # Company:

    # Filtering to get all uncompleted UAL where manager = user (Subordinates)
    employee_midyear_list_database = User_Appraisal_List.objects.filter(overall_appraisal__status__contains='Stage 1B')

    # Filtering to get all UAL with stage = 1 where user!=HR (Employees)
    employee_GCS_list_database = User_Appraisal_List.objects.filter(overall_appraisal__status__contains='Stage 1')

    # Filtering to get all UAL with stage = 2 where user!=HR (Employees)
    employee_appraisal_list_database = User_Appraisal_List.objects.filter(overall_appraisal__status__contains='Stage 2')

    # Filtering to get all UAL with stage = 3 where user!=HR (Employees)
    employee_reports_list_database = User_Appraisal_List.objects.filter(overall_appraisal__status__contains='Stage 3')

    # Filtering to get all UAL with stage = 4 where user!=HR (Employees)
    employee_calibration_list_database = User_Appraisal_List.objects.filter(
        overall_appraisal__status__contains='Stage 4')

    # Filtering to get all subordinate UAL
    employee_appraisal_system_database = User_Appraisal_List.objects.all().order_by('overall_appraisal__status')

    # Company: Reports
    # Filtering to get all stage 3 / 4 / completed OAs
    records_overall_appraisal_database = Overall_Appraisal.objects.filter(
        Q(status='Stage 3') | Q(status='Stage 4') | Q(status='Completed'))

    # Employee Management
    # !Filtering to get all profiles excluding HR department
    company_profile_database = Profile.objects.exclude(department=request.user.profile.department).order_by('name')
    # !Filtering to get all OA excluding completed ones
    company_appraisal_database = Overall_Appraisal.objects.exclude(status='Completed')
    # !Filtering to get all completed OAs
    company_completed_appraisal_database = Overall_Appraisal.objects.filter(status='Completed')
    # Reports
    records_user_appraisal_database = User_Appraisal_List.objects.filter(
        overall_appraisal__status__contains='Completed', employee=request.user.profile)

    context = {
        # Get all Goals Setting OA of user:
        "rubic1": rubric_overall_appraisal_database1,
        # Get all Mid Year OA of user:
        "rubic2": rubric_overall_appraisal_database2,
        # Get all End Year OA of user:
        "rubic3": rubric_overall_appraisal_database3,
        # !Get all UAL with same managers that are undergoing appraisal stage, excluding personal UALs
        "user_appraisal_list": user_appraisal_database,
        # !Get profile of user's manager
        "req_user_manager": user_manager_database,

        # !Get all UAL with same managers that are undergoing appraisal stage, excluding personal UALs
        "user_appraisal_list_database": user_appraisal_list_database,
        # Get all peerAppraisals with viewers = user
        "peer_appraisal_database": peer_appraisal_database,

        # !Get all profiles excluding HR department
        "company_profile_database": company_profile_database,
        # !Get all OA excluding completed ones
        "company_appraisal_database": company_appraisal_database,
        # !Get all completed OAs
        "company_completed_appraisal_database": company_completed_appraisal_database,

        # Get all UAL with stage = 1 where manager = user (Subordinates)
        "subordinate_GCS_database": employee_GCS_list_database,
        # Get all uncompleted UAL where manager = user (Subordinates)
        "employee_midyear_database": employee_midyear_list_database,
        # Get all UAL with stage = 2 where manager = user (Subordinates)
        "department_appraisal_database": employee_appraisal_list_database,
        # Get all UAL with stage = 3 where manager = user (Subordinates)
        "department_reports_database": employee_reports_list_database,
        # Get all UAL with stage = 4 where manager = user (Subordinates)
        "department_calibration_database": employee_calibration_list_database,

        "company_records_database": records_overall_appraisal_database,

        # !Get all subordinate UAL
        "department_entire_subUAL_database": employee_appraisal_system_database,
        # Reports
        "records_UAL_database": records_user_appraisal_database

    }
    return render(request, 'login2/HuNetHR_Dashboard3.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['HR manager'])
def HRmanager_dashboard(request):
    # Dashboard Rubrics
    # !Filter to get all Goals Setting OA of user:
    rubric_overall_appraisal_database1 = Overall_Appraisal.objects.distinct().filter(
        user_appraisal_list__employee=request.user.profile, status='Stage 1').count

    # !Filter to get all Mid Year Review OA of user:
    rubric_overall_appraisal_database2 = Overall_Appraisal.objects.filter(
        user_appraisal_list__employee=request.user.profile, status='Stage 1B').count

    # !Filter to get all End Year OA of user:
    rubric_overall_appraisal_database3 = Overall_Appraisal.objects.filter(
        Q(status='Stage 2') | Q(status='Stage 3') | Q(status='Stage 4'),
        user_appraisal_list__employee=request.user.profile, ).count

    # Dashboard user
    # !Filtering to get all uncompleted UAL of users
    user_appraisal_database = User_Appraisal_List.objects.filter(employee=request.user.profile).exclude(
        overall_appraisal__status__contains='Completed')

    # !Filtering to get profile of user's manager
    user_manager_database = Profile.objects.get(user=request.user).first_Reporting_Manager

    # Peer appraisal:
    # !Filtering to get all UAL with same managers that are undergoing appraisal stage, excluding personal UALs
    user_appraisal_list_database = User_Appraisal_List.objects.filter(
        manager=request.user.profile.first_Reporting_Manager, overall_appraisal__status__contains='Stage 2').exclude(
        employee=request.user.profile)

    # !Filtering to get all peerAppraisals with viewers = user
    peer_appraisal_database = peerAppraisal.objects.filter(viewer=request.user.profile).order_by('-completion')

    # Department:
    # !Filtering to get all profile where manager = user (Subordinates)
    subordinates_database = Profile.objects.filter(first_Reporting_Manager=request.user.profile)

    # !Filtering to get Overall Appraisals in Stage 1
    subordinate_GCS_appraisal_database = Overall_Appraisal.objects.filter(Q(status='Stage 1') | Q(status='Stage 2'))

    # Filtering to get all UAL with stage = 1 where manager = user (Subordinates)
    subordinate_GCS_list_database = User_Appraisal_List.objects.filter(overall_appraisal__status__contains='Stage 1',
                                                                       manager=request.user.profile)

    # Filtering to get all uncompleted UAL where manager = user (Subordinates)
    subordinate_midyear_list_database = User_Appraisal_List.objects.filter(
        overall_appraisal__status__contains='Stage 1B', manager=request.user.profile)

    # Filtering to get all UAL with stage = 2 where manager = user (Subordinates)
    subordinate_appraisal_list_database = User_Appraisal_List.objects.filter(
        overall_appraisal__status__contains='Stage 2', manager=request.user.profile)

    # Filtering to get all UAL with stage = 3 where manager = user (Subordinates)
    subordinate_reports_list_database = User_Appraisal_List.objects.filter(
        overall_appraisal__status__contains='Stage 3', manager=request.user.profile)

    # Filtering to get all UAL with stage = 4 where manager = user (Subordinates)
    subordinate_calibration_list_database = User_Appraisal_List.objects.filter(
        overall_appraisal__status__contains='Stage 4', manager=request.user.profile)

    # Filtering to get all subordinate uncompleted UAL
    subordinate_appraisal_system_database = User_Appraisal_List.objects.filter(manager=request.user.profile).order_by(
        'employee', 'overall_appraisal__status')

    # !Filtering to get all departmental goals with manager = user + excluding completed OA
    MCreated_DG_database = Departmental_Goals.objects.filter(manager=request.user.profile).exclude(
        appraisal__status__contains='Completed')
    # !Filtering to get all departmental competencies with manager = user + excluding completed OA
    MCreated_DC_database = Departmental_Competencies.objects.filter(manager=request.user.profile).exclude(
        appraisal__status__contains='Completed')

    # Company:

    # Filtering to get all uncompleted UAL where manager = user (Subordinates)
    employee_midyear_list_database = User_Appraisal_List.objects.filter(overall_appraisal__status__contains='Stage 1B')

    # Filtering to get all UAL with stage = 1 where user!=HR (Employees)
    employee_GCS_list_database = User_Appraisal_List.objects.filter(overall_appraisal__status__contains='Stage 1')

    # Filtering to get all UAL with stage = 2 where user!=HR (Employees)
    employee_appraisal_list_database = User_Appraisal_List.objects.filter(overall_appraisal__status__contains='Stage 2')

    # Filtering to get all UAL with stage = 3 where user!=HR (Employees)
    employee_reports_list_database = User_Appraisal_List.objects.filter(overall_appraisal__status__contains='Stage 3')

    # Filtering to get all UAL with stage = 4 where user!=HR (Employees)
    employee_calibration_list_database = User_Appraisal_List.objects.filter(
        overall_appraisal__status__contains='Stage 4')

    # Filtering to get all subordinate UAL
    employee_appraisal_system_database = User_Appraisal_List.objects.all().order_by('overall_appraisal__status')

    # Company: Reports
    # Filtering to get all stage 3 / 4 / completed OAs
    records_overall_appraisal_database = Overall_Appraisal.objects.filter(
        Q(status='Stage 3') | Q(status='Stage 4') | Q(status='Completed'))

    # Employee Management
    # !Filtering to get all profiles excluding HR department
    company_profile_database = Profile.objects.all().order_by('name')
    # !Filtering to get all OA excluding completed ones
    company_appraisal_database = Overall_Appraisal.objects.exclude(status='Completed')
    # !Filtering to get all completed OAs
    company_completed_appraisal_database = Overall_Appraisal.objects.filter(status='Completed')

    records_user_appraisal_database = User_Appraisal_List.objects.filter(
        overall_appraisal__status__contains='Completed', employee=request.user.profile)

    context = {
        # Get all Goals Setting OA of user:
        "rubic1": rubric_overall_appraisal_database1,
        # Get all Mid Year OA of user:
        "rubic2": rubric_overall_appraisal_database2,
        # Get all End Year OA of user:
        "rubic3": rubric_overall_appraisal_database3,

        # !Get all UAL with same managers that are undergoing appraisal stage, excluding personal UALs
        "user_appraisal_list": user_appraisal_database,
        # !Get profile of user's manager
        "req_user_manager": user_manager_database,

        # !Get all UAL with same managers that are undergoing appraisal stage, excluding personal UALs
        "user_appraisal_list_database": user_appraisal_list_database,
        # Get all peerAppraisals with viewers = user
        "peer_appraisal_database": peer_appraisal_database,

        # !Get all profile where manager = user (Subordinates)
        "subordinate_database": subordinates_database,
        # !Get all Overall Appraisals
        "department_GCS_database": subordinate_GCS_appraisal_database,
        # Get all UAL with stage = 1 where manager = user (Subordinates)
        "subordinate_GCS_database": subordinate_GCS_list_database,
        # Get all uncompleted UAL where manager = user (Subordinates)
        "subordinate_midyear_database": subordinate_midyear_list_database,
        # Get all UAL with stage = 2 where manager = user (Subordinates)
        "department_appraisal_database": subordinate_appraisal_list_database,
        # Get all UAL with stage = 3 where manager = user (Subordinates)
        "department_reports_database": subordinate_reports_list_database,
        # Get all UAL with stage = 4 where manager = user (Subordinates)
        "department_calibration_database": subordinate_calibration_list_database,
        # !Get all subordinate UAL
        "department_entire_subUAL_database": subordinate_appraisal_system_database,
        # !Get all departmental goals with manager = user + excluding completed OA
        "mcreated_dg_database": MCreated_DG_database,
        # !Get all departmental competencies with manager = user + excluding completed OA
        "mcreated_dc_database": MCreated_DC_database,

        # Company
        # !Get all profiles excluding HR department
        "company_profile_database": company_profile_database,
        # !Get all OA excluding completed ones
        "company_appraisal_database2": company_appraisal_database,
        # !Get all completed OAs
        "company_completed_appraisal_database": company_completed_appraisal_database,

        # Get all UAL with stage = 1
        "company_GCS_database": employee_GCS_list_database,
        # Get all uncompleted UAL
        "company_midyear_database": employee_midyear_list_database,
        # Get all UAL with stage = 2
        "company_appraisal_database": employee_appraisal_list_database,
        # Get all UAL with stage = 3
        "company_reports_database": employee_reports_list_database,
        # Get all UAL with stage = 4
        "company_calibration_database": employee_calibration_list_database,

        "company_records_database": records_overall_appraisal_database,
        # !Get all subordinate UAL
        "company_entire_subUAL_database": employee_appraisal_system_database,
        # Reports
        "records_UAL_database": records_user_appraisal_database
    }
    return render(request, 'login2/HuNetHRM_Dashboard4.html', context)


@login_required(login_url='login')
def Create_Profile(request, *args, **kwargs):
    form = CreateProfileForm
    email_string = ""
    user_username = ""
    lowered_username = ""
    final_username = ""
    if request.method == 'POST':
        promotion_type = request.POST.get('promotion')

        form = CreateProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            user_username += profile.name
            lowered_username += user_username.lower()
            final_username += lowered_username.replace(' ', '')

            user_password = 'DenselightPassword1234'
            user_email = profile.email

            userprofile, user_created = User.objects.update_or_create(
                username=final_username,
                password=make_password(user_password),
                email=user_email,
                is_active=True,
            )

            if user_created:
                if promotion_type == 'Employee':
                    group = Group.objects.get(name='Employee')

                    userprofile.groups.add(group)

                elif promotion_type == 'Manager':
                    group = Group.objects.get(name='Manager')

                    userprofile.groups.add(group)

                elif promotion_type == 'HR':
                    group = Group.objects.get(name='HR')
                    userprofile.groups.add(group)

                elif promotion_type == 'HR manager':
                    group = Group.objects.get(name='HR manager')
                    userprofile.groups.add(group)

                else:
                    group = Group.objects.get(name='Employee')

                    userprofile.groups.add(group)
                profile.user = userprofile

                try:
                    email_string = PROFILE_CREATION_EMAIL(profile.name, userprofile.username, profile.email,
                                                          profile.typeOfEmployee)
                    send_mail('Performance Management System Login Details', email_string,
                              from_email='denselight_epmp@consulthunet.com', recipient_list=[profile.email],
                              fail_silently=True)
                except Exception:
                    pass
                profile.save()
                profileid = profile.id
                return HttpResponseRedirect(reverse('Detail_Profile_HR', args=(profileid,)))
        else:
            messages.warning(request, 'Creation invalid. \n Please key in compulsory fields.')
            messages.warning(request, 'Ensure that country code is added to phone field.')

    context = {
        'form': form
    }

    return render(request, 'login2/HR_CreateProfile.html', context)


@login_required(login_url='login')
def Update_Profile(request, *args, **kwargs):
    id = kwargs.get('pk')
    profile_user = Profile.objects.get(id=id)

    supermanager_group = Group.objects.get(name='HR manager')
    supermanager_user = User.objects.filter(groups=supermanager_group)

    email_string = ""
    listOfEmails = []

    try:
        for euser in supermanager_user:
            listOfEmails.append(euser.profile.email)
    except Exception:
        pass

    form = UpdateProfileForm_All(request.POST or None, instance=profile_user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            try:
                email_string = PROFILE_UPDATE_EMAIL(profile_user)
                send_mail('Profile Change', email_string, from_email='denselight_epmp@consulthunet.com',
                          recipient_list=listOfEmails, fail_silently=True)
            except Exception:
                pass
            return HttpResponseRedirect(reverse('Detail_Profile', args=(profile_user.id,)))

        else:
            messages.warning(request, 'Creation invalid. \n Please key in compulsory fields.')
            messages.warning(request, 'Ensure that country code is added to phone field.')

    context = {
        'form': form,
        'object': profile_user
    }

    return render(request, 'login2/UpdateProfile.html', context)


@login_required(login_url='login')
def Update_Profile_HR(request, *args, **kwargs):
    id = kwargs.get('pk')
    profile_user = Profile.objects.get(id=id)

    form = CreateProfileForm(request.POST or None, instance=profile_user)
    if request.method == 'POST':
        promotion_type = request.POST.get('promotion')
        if form.is_valid():
            savestatus = form.save()

            if savestatus:

                if promotion_type == 'Employee':
                    if request.user.groups.exists():
                        try:
                            user_group = profile_user.user.groups.all()[0].id
                            profile_user.user.groups.remove(user_group)
                        except:
                            pass
                    group = Group.objects.get(name='Employee')
                    profile_user.user.groups.add(group)

                elif promotion_type == 'Manager':
                    if request.user.groups.exists():
                        try:
                            user_group = profile_user.user.groups.all()[0].id
                            profile_user.user.groups.remove(user_group)
                        except:
                            pass

                    group = Group.objects.get(name='Manager')
                    profile_user.user.groups.add(group)

                elif promotion_type == 'HR':
                    if request.user.groups.exists():
                        try:
                            user_group = profile_user.user.groups.all()[0].id
                            profile_user.user.groups.remove(user_group)
                        except:
                            pass
                    group = Group.objects.get(name='HR')
                    profile_user.user.groups.add(group)

                elif promotion_type == 'HR manager':
                    if request.user.groups.exists():
                        try:
                            user_group = profile_user.user.groups.all()[0].id
                            profile_user.user.groups.remove(user_group)
                        except:
                            pass
                    group = Group.objects.get(name='HR manager')
                    profile_user.user.groups.add(group)

            return HttpResponseRedirect(reverse('Detail_Profile_HR', args=(profile_user.id,)))

        else:
            messages.warning(request, 'Creation invalid. \n Please key in compulsory fields.')
            messages.warning(request, 'Ensure that country code is added to phone field.')
    context = {
        'form': form
    }

    return render(request, 'login2/HR_UpdateProfile.html', context)


@login_required(login_url='login')
def Detail_Profile(request, *args, **kwargs):
    id = kwargs.get('pk')
    user_profile = Profile.objects.get(id=id)

    # Overall Appraisals Completed
    records_user_appraisal_database = User_Appraisal_List.objects.filter(
        overall_appraisal__status__contains='Completed', employee=user_profile)

    qualifications_database = Qualifications.objects.filter(employee=user_profile).order_by('-id')[:5]
    profile_skills_database1 = Skills.objects.filter(employee=user_profile).order_by('-id')[:3]
    profile_skills_database2 = Skills.objects.filter(employee=user_profile).order_by('-id')[3:6]

    context = {
        'object': user_profile,
        'comp_overall_appraisal_database': records_user_appraisal_database,
        'qualifications_database': qualifications_database,
        'profile_skills_database1': profile_skills_database1,
        'profile_skills_database2': profile_skills_database2
    }
    return render(request, 'login2/All_DetailProfile.html', context)


@login_required(login_url='login')
def Detail_Profile_HR(request, *args, **kwargs):
    id = kwargs.get('pk')
    user_profile = Profile.objects.get(id=id)

    # Overall Appraisals Completed
    records_user_appraisal_database = User_Appraisal_List.objects.filter(
        overall_appraisal__status__contains='Completed', employee=user_profile)

    qualifications_database = Qualifications.objects.filter(employee=user_profile).order_by('-id')[:5]
    profile_skills_database1 = Skills.objects.filter(employee=user_profile).order_by('-id')[:3]
    profile_skills_database2 = Skills.objects.filter(employee=user_profile).order_by('-id')[3:6]

    context = {
        'object': user_profile,
        'comp_overall_appraisal_database': records_user_appraisal_database,
        'qualifications_database': qualifications_database,
        'profile_skills_database1': profile_skills_database1,
        'profile_skills_database2': profile_skills_database2
    }
    return render(request, 'login2/HR_DetailProfile.html', context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class Create_Qualifications(CreateView):
    model = Qualifications
    form_class = CreateQualificationsForm
    template_name = 'login2/Create_Qualifications.html'

    def get_success_url(self):
        return reverse('Detail_Profile', kwargs={'pk': self.kwargs['pk']})

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Qualifications, id=id)

    def form_valid(self, form):
        id = self.kwargs.get('pk')
        user_profile = Profile.objects.get(id=id)
        form.instance.employee = user_profile
        print(form.cleaned_data)
        return super(Create_Qualifications, self).form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class Create_Qualifications_HR(CreateView):
    model = Qualifications
    form_class = CreateQualificationsForm
    template_name = 'login2/Create_Qualifications.html'

    def get_success_url(self):
        return reverse('Detail_Profile_HR', kwargs={'pk': self.kwargs['pk']})

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Qualifications, id=id)

    def form_valid(self, form):
        id = self.kwargs.get('pk')
        user_profile = Profile.objects.get(id=id)
        form.instance.employee = user_profile
        print(form.cleaned_data)
        return super(Create_Qualifications_HR, self).form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class Delete_Qualifications(DeleteView):
    model = Qualifications
    template_name = 'login2/Delete_Qualifications.html'

    def get_success_url(self):
        return reverse('Detail_Profile', kwargs={'pk': self.kwargs['pk']})

    def get_object(self):
        id = self.kwargs.get("mk")
        return get_object_or_404(Qualifications, id=id)


@method_decorator(login_required(login_url='login'), name='dispatch')
class Delete_Qualifications_HR(DeleteView):
    model = Qualifications
    template_name = 'login2/Delete_Qualifications.html'

    def get_success_url(self):
        return reverse('Detail_Profile_HR', kwargs={'pk': self.kwargs['pk']})

    def get_object(self):
        id = self.kwargs.get("mk")
        return get_object_or_404(Qualifications, id=id)


# @csrf_exempt
# def savekpi(request):
#     id=request.POST.get('id', '')
#     type=request.POST.get('type', '')
#     value=request.POST.get('value', '')
#     kpi = KPI.objects.get(id=id)
#     if type == "progress":
#         kpi.progress = value
#     kpi.save()
#     return JsonResponse({"success": "Updated"})

@permission_required('admin.can_add_log_entry')
@login_required(login_url='login')
def Profile_Upload(request):
    global profile_created
    lastuser = ""
    counter = 0
    # Context variable, tell them order of files
    context = {
        'order': 'Order of CSV should be name, email, message'
    }

    if request.method == 'GET':
        return render(request, "login2/Profile_Upload.html", context)

    csv_file = request.FILES['file']
    # Check if its a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    # Avoid header
    next(io_string)
    # if have quotes, quotechar escapes them
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _id = randint(0, 2147483647)
        email_string = ""
        stringed_username = column[1]
        lowered_username = stringed_username.lower()
        lowered_username = lowered_username.replace(' ', '').replace('(', '').replace(')', '').replace(',', '')
        try:
            profileuser, user_created = User.objects.update_or_create(
                username=lowered_username,
                password=make_password('DenselightPassword1234'),
                email=column[6],
                is_active=True,
            )
            counter += 1
            lastuser += str(counter) + ". " + lowered_username + ", "
        except Exception:
            if lastuser == "":
                lastuser = "No profiles created"
            messages.info(request, 'Users Created: ' + lastuser)
            break

        created = False
        user_created = False

        alldepartments = Departments.objects.all()
        userdepartment = alldepartments[0]
        departmentname = ""
        departmentname += column[4]
        if departmentname != "":
            try:
                userdepartment = Departments.objects.get(name=departmentname)
            except Exception:
                department_created = Departments(
                    name=departmentname,
                    id=_id
                )
                userdepartment = department_created.save()

        elif departmentname == "":
            userdepartment = alldepartments[0]

        try:
            userdepartment = Departments.objects.get(name=departmentname)
        except Exception:
            pass

        manager_name = ""
        manager_name += column[7]
        manager_profile = Profile.objects.all()[0]
        try:
            manager_profile = Profile.objects.get(name=manager_name)
        except Exception:
            pass

        HOD_name = ""
        HOD_name += column[8]

        try:
            profile_created = Profile(
                user=profileuser,
                employee_ID=column[0],
                name=column[1],
                typeOfEmployee=column[2],
                job_Title=column[3],
                email=column[6],
                department=userdepartment,
                first_Reporting_Manager=manager_profile,
                second_Reporting_Manager=HOD_name,
                date_Of_Hire=column[5],
                id=_id
            )
            profile_created.save()
            created = True
        except:
            pass

        access_type = ''
        access_type += column[9]
        lowered_access_type = access_type.lower()
        if lowered_access_type == 'employee':
            group = Group.objects.get(name='Employee')
            profileuser.groups.add(group)
        elif lowered_access_type == 'manager':
            group = Group.objects.get(name='Manager')
            profileuser.groups.add(group)
        elif lowered_access_type == 'hr':
            group = Group.objects.get(name='HR')
            profileuser.groups.add(group)
        elif lowered_access_type == 'hr manager':
            group = Group.objects.get(name='HR manager')
            profileuser.groups.add(group)
        else:
            pass

        if created and user_created:
            try:
                email_string = PROFILE_CREATION_EMAIL(profile_created.name, profileuser.username, profile_created.email,
                                                      profile_created.typeOfEmployee)
                send_mail('Performance Management System Login Details', email_string,
                          from_email='denselight_epmp@consulthunet.com', recipient_list=[profile_created.email],
                          fail_silently=True)
            except Exception:
                pass

    context = {}
    return render(request, "login2/Profile_Upload.html", context)
