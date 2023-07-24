from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer
from .forms import EmployeeUpdateForm

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

def employee_update(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')  # Redirect to the employee list page
    else:
        form = EmployeeUpdateForm(instance=employee)
    return render(request, 'employees/employee_update.html', {'form': form})
