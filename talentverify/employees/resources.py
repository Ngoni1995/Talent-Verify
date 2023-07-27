# employees/resources.py

from import_export import resources
from .models import Employee

class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        fields = ('employee_id', 'name', 'department', 'role', 'date_started', 'date_left', 'duties')
