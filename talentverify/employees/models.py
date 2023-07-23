from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    date_started = models.DateField()
    date_left = models.DateField(blank=True, null=True)
    duties = models.TextField(blank=True)

    def __str__(self):
        return self.name
