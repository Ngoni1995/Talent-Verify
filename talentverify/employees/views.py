
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from io import StringIO
from pandas.errors import EmptyDataError

from django.http import Http404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer
from .forms import EmployeeUpdateForm, EmployeeBulkUpdateForm
import pandas as pd
from django.contrib import messages
from .models import Company, Employee
from .forms import CompanyForm, EmployeeForm
from .forms import EmployeeForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


def home(request):
    return render(request, 'talentverify/home.html')


def employee_list(request):
    employees = Employee.objects.all()

    # Search functionality
    query_name = request.GET.get('name')
    query_employer = request.GET.get('employer')
    query_position = request.GET.get('position')
    query_department = request.GET.get('department')
    query_year_started = request.GET.get('year_started')
    query_year_left = request.GET.get('year_left')

    if query_name:
        employees = employees.filter(name__icontains=query_name)

    if query_employer:
        employees = employees.filter(employer__icontains=query_employer)

    if query_position:
        employees = employees.filter(position__icontains=query_position)

    if query_department:
        employees = employees.filter(department__icontains=query_department)

    if query_year_started:
        employees = employees.filter(year_started=query_year_started)

    if query_year_left:
        employees = employees.filter(year_left=query_year_left)

    return render(request, 'employees/employee_list.html', {'employees': employees})

def employee_update(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        raise Http404("Employee does not exist.")

    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee information updated successfully.')
            return redirect('employee_list')  # Redirect to the employee list page after single-entry update
        else:
            messages.error(request, 'Error occurred. Please check the form fields.')
    else:
        form = EmployeeUpdateForm(instance=employee)

    return render(request, 'employees/employee_update.html', {'form': form})

def employee_update_single(request, employee_id=None):
    try:
        if employee_id is not None:
            employee = Employee.objects.get(id=employee_id)
        else:
            employee = None

        if request.method == 'POST':
            form = EmployeeUpdateForm(request.POST, instance=employee)
            if form.is_valid():
                employee = form.save(commit=False)
                if 'company' in request.POST:
                    employee.company = Company.objects.get(id=request.POST['company'])
                employee.save()
                messages.success(request, 'Employee information updated successfully.')
                return redirect('employee_list')
            else:
                messages.error(request, 'Error occurred. Please check the form fields.')
        else:
            form = EmployeeUpdateForm(instance=employee)

        companies = Company.objects.all()  # Get all companies to pass to the template
        return render(request, 'employees/employee_update_single.html', {'form': form, 'companies': companies})

    except Employee.DoesNotExist:
        raise Http404("Employee does not exist.")
    
import csv

def bulk_update_employees(request):
    if request.method == 'POST':
        form = EmployeeBulkUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            employees_file = request.FILES['file']
            try:
                # Read the file as a string
                file_content = employees_file.read().decode('utf-8')
                print(file_content)

                # Convert the string to a list of lists using CSV reader
                rows = csv.reader(file_content.splitlines())
                
                # Skip the header row (employee_id, name, department, etc.)
                next(rows)

                for row in rows:
                    employee_id = row[0]  # Assuming 'employee_id' is the first column in the CSV file
                    employee, created = Employee.objects.get_or_create(employee_id=employee_id)
                    for i, field_name in enumerate(['name', 'department', 'role', 'date_started', 'date_left', 'duties']):
                        setattr(employee, field_name, row[i+1])  # Skip the first element as it's 'employee_id'
                    employee.save()
                messages.success(request, 'Employee information updated in bulk successfully.')
                return redirect('employee_list')  # Redirect to the employee list page after bulk update
            except Exception as e:
                messages.error(request, f'Error occurred during bulk update: {e}')
        else:
            messages.error(request, 'Form is invalid. Please check the form fields.')
    else:
        form = EmployeeBulkUpdateForm()
    return render(request, 'employees/bulk_update_employees.html', {'form': form})


#talent-verify Admins








def talent_verify_admin_update_single(request, employee_id=None):
    try:
        if employee_id is not None:
            employee = Employee.objects.get(id=employee_id)
        else:
            employee = None

        if request.method == 'POST':
            form = EmployeeUpdateForm(request.POST, instance=employee)
            if form.is_valid():
                form.save()
                messages.success(request, 'Employee information updated successfully.')
                return redirect('employee_list')  # Redirect to the employee list page after single-entry update
            else:
                messages.error(request, 'Error occurred. Please check the form fields.')
        else:
            form = EmployeeUpdateForm(instance=employee)
    except Employee.DoesNotExist:
        raise Http404("Employee does not exist.")  # Handle the case when employee with given ID does not exist

    return render(request, 'employees/talent_verify_admin_update_single.html', {'form': form})

def talent_verify_admin_bulk_update(request):
    if request.method == 'POST':
        form = EmployeeBulkUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            employees_file = request.FILES['file']
            df = pd.read_csv(employees_file)
            for index, row in df.iterrows():
                employee_id = row['employee_id']
                employee, created = Employee.objects.get_or_create(employee_id=employee_id)
                for field_name in ['name', 'department', 'role', 'date_started', 'date_left', 'duties']:
                    setattr(employee, field_name, row[field_name])
                employee.save()
                messages.success(request, 'Employee information updated in bulk successfully.')
                return redirect('employee_list')  # Redirect to the employee list page after bulk update
        else:
            messages.error(request, 'Form is invalid. Please check the form fields.')
    else:
        form = EmployeeBulkUpdateForm()
    return render(request, 'employees/talent_verify_admin_bulk_update.html', {'form': form})

def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyForm()
    return render(request, 'talentverify/add_company.html', {'form': form})

def add_employee(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.company = company
            employee.save()
            return redirect('company_detail', company_id=company.id)
    else:
        form = EmployeeForm()

    return render(request, 'talentverify/add_employee.html', {'form': form, 'company': company})


def company_list(request):
    companies = Company.objects.all()
    return render(request, 'talentverify/company_list.html', {'companies': companies})

def company_detail(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    employees = company.employee_set.all()
    return render(request, 'talentverify/company_detail.html', {'company': company, 'employees': employees})

def company_login(request):
    if request.method == 'POST':
        # Retrieve the username and password from the form
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if the user belongs to the Company Users group (you can customize this based on your group names)
            if user.groups.filter(name='Company Users').exists():
                # Login the user
                login(request, user)
                return HttpResponseRedirect(reverse('company_dashboard'))
            else:
                # If the user does not belong to the Company Users group, show an error message
                return render(request, 'accounts/company_login.html', {'error_message': 'Invalid login credentials.'})
        else:
            # If authentication fails, show an error message
            return render(request, 'accounts/company_login.html', {'error_message': 'Invalid login credentials.'})
    else:
        # If it's a GET request, show the login form
        return render(request, 'accounts/company_login.html')

def talent_verify_login(request):
    if request.method == 'POST':
        # Retrieve the username and password from the form
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if the user belongs to the Talent Verify group (you can customize this based on your group names)
            if user.groups.filter(name='Talent Verify').exists():
                # Login the user
                login(request, user)
                return HttpResponseRedirect(reverse('talent_verify_dashboard'))
            else:
                # If the user does not belong to the Talent Verify group, show an error message
                return render(request, 'accounts/talent_verify_login.html', {'error_message': 'Invalid login credentials.'})
        else:
            # If authentication fails, show an error message
            return render(request, 'accounts/talent_verify_login.html', {'error_message': 'Invalid login credentials.'})
    else:
        # If it's a GET request, show the login form
        return render(request, 'accounts/talent_verify_login.html')

def general_users_login(request):
    if request.method == 'POST':
        # Retrieve the username and password from the form
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if the user belongs to the General Users group (you can customize this based on your group names)
            if user.groups.filter(name='General Users').exists():
                # Login the user
                login(request, user)
                return HttpResponseRedirect(reverse('general_users_dashboard'))
            else:
                # If the user does not belong to the General Users group, show an error message
                return render(request, 'accounts/general_users_login.html', {'error_message': 'Invalid login credentials.'})
        else:
            # If authentication fails, show an error message
            return render(request, 'accounts/general_users_login.html', {'error_message': 'Invalid login credentials.'})
    else:
        # If it's a GET request, show the login form
        return render(request, 'accounts/general_users_login.html')

def company_dashboard(request):
    # Add logic for Company Users' dashboard here
    # For example, you can retrieve and display specific information for Company Users
    return render(request, 'accounts/company_dashboard.html')

def talent_verify_dashboard(request):
    # Add logic for Talent Verify dashboard here
    # For example, you can retrieve and display specific information for Talent Verify
    return render(request, 'accounts/talent_verify_dashboard.html')

def general_users_dashboard(request):
    # Add logic for General Users dashboard here
    # For example, you can retrieve and display specific information for General Users
    return render(request, 'accounts/general_users_dashboard.html')
