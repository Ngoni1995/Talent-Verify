from django import forms
from .models import Employee
from django.core import validators
from .models import Company, Employee

class SelectCompanyForm(forms.Form):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), label='Select a Company')

class EmployeeBulkUpdateForm(forms.Form):
    file = forms.FileField(label='Upload CSV, Text, or Excel file')


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'department', 'role', 'date_started', 'date_left', 'duties']
        name = forms.CharField(validators=[validators.RegexValidator(r'^[a-zA-Z\s]*$', 'Only alphabetic characters are allowed.')])
    # Add similar validators for other fields that require alphabetic characters only

class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'employee_id', 'department', 'role', 'date_started', 'date_left', 'duties']



class EmployeeBulkUpdateForm(forms.Form):
    file = forms.FileField(label='Upload CSV, Text, or Excel file')



class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

