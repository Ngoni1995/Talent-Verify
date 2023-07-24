from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer
from .forms import EmployeeUpdateForm, EmployeeBulkUpdateForm
import pandas as pd
from django.contrib import messages

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

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
                form.save()
                messages.success(request, 'Employee information updated successfully.')
                return redirect('employee_list')  # Redirect to the employee list page after single-entry update
            else:
                messages.error(request, 'Error occurred. Please check the form fields.')
        else:
            form = EmployeeUpdateForm(instance=employee)
    except Employee.DoesNotExist:
        raise Http404("Employee does not exist.")  # Handle the case when employee with given ID does not exist

    return render(request, 'employees/employee_update_single.html', {'form': form})

def bulk_update_employees(request):
    if request.method == 'POST':
        form = EmployeeBulkUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            employees_file = request.FILES['file']
            try:
                df = pd.read_csv(employees_file)  # Assuming the file is in CSV format, you can modify accordingly for other formats
                for index, row in df.iterrows():
                    employee_id = row['employee_id']  # Assuming 'employee_id' is the column name in the CSV file
                    employee, created = Employee.objects.get_or_create(employee_id=employee_id)
                    for field_name in ['name', 'department', 'role', 'date_started', 'date_left', 'duties']:
                        setattr(employee, field_name, row[field_name])
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
            try:
                df = pd.read_csv(employees_file)  # Assuming the file is in CSV format, you can modify accordingly for other formats
                for index, row in df.iterrows():
                    employee_id = row['employee_id']  # Assuming 'employee_id' is the column name in the CSV file
                    employee, created = Employee.objects.get_or_create(employee_id=employee_id)
                    for field_name in ['name', 'department', 'role', 'date_started', 'date_left', 'duties']:
                        setattr(employee, field_name, row[field_name])
                    employee.save()
                messages.success(request, 'Employee information updated in bulk successfully.')
                return redirect('employee_list')  # Redirect to the employee list page after bulk update
            except Exception as e:
                messages.error(request, f'Error occurred during bulk update: {e}')
        else:
            messages.error(request, 'Form is invalid. Please check the form fields.')
    else:
        form = EmployeeBulkUpdateForm()
    return render(request, 'employees/talent_verify_admin_bulk_update.html', {'form': form})