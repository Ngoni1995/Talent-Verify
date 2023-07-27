
from django.db import models
from import_export import resources




class Company(models.Model):
    name = models.CharField(max_length=100)
    date_of_registration = models.DateField()
    company_registration_number = models.CharField(max_length=50)
    address = models.TextField()
    contact_person = models.CharField(max_length=100)
    departments = models.TextField()
    number_of_employees = models.PositiveIntegerField()
    contact_phone = models.CharField(max_length=20)
    email_address = models.EmailField()

    def __str__(self):
        return self.name

class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)  # Make sure the foreign key is correctly defined.
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    date_started = models.DateField()
    date_left = models.DateField(blank=True, null=True)
    duties = models.TextField(blank=True)

    def __str__(self):
        return self.name

class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        fields = ('employee_id', 'name', 'department', 'role', 'date_started', 'date_left', 'duties')