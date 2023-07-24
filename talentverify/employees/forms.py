from django import forms
from .models import Employee

class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'employee_id', 'department', 'role', 'date_started', 'date_left', 'duties']



class EmployeeBulkUpdateForm(forms.Form):
    file = forms.FileField(label='Upload CSV, Text, or Excel file')
