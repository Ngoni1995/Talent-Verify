from django.test import TestCase
from django.urls import reverse
from .models import Employee
from .forms import EmployeeUpdateForm

class EmployeeUpdateTest(TestCase):
    def setUp(self):
        # Create a sample employee
        self.employee = Employee.objects.create(
            name='John Doe',
            employee_id='EMP001',
            department='HR',
            role='Manager',
            date_started='2023-01-01',
        )

    def test_employee_update_view(self):
        url = reverse('employee_update', args=[self.employee.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Update Employee Information')
        self.assertIsInstance(response.context['form'], EmployeeUpdateForm)

        # Test updating employee information
        updated_data = {
            'name': 'John Smith',
            'employee_id': 'EMP002',
            'department': 'Finance',
            'role': 'Accountant',
            'date_started': '2022-12-01',
            'date_left': '2023-06-30',
            'duties': 'Financial reporting',
        }
        response = self.client.post(url, data=updated_data)
        self.assertRedirects(response, reverse('employee_list'))

        # Check that the employee data has been updated in the database
        updated_employee = Employee.objects.get(id=self.employee.id)
        self.assertEqual(updated_employee.name, 'John Smith')
        self.assertEqual(updated_employee.employee_id, 'EMP002')
        self.assertEqual(updated_employee.department, 'Finance')
        self.assertEqual(updated_employee.role, 'Accountant')
        self.assertEqual(str(updated_employee.date_started), '2022-12-01')
        self.assertEqual(str(updated_employee.date_left), '2023-06-30')
        self.assertEqual(updated_employee.duties, 'Financial reporting')

class TalentVerifyAdminUpdateSingleTest(TestCase):
    def setUp(self):
        # Create a sample employee
        self.employee = Employee.objects.create(
            name='John Doe',
            employee_id='EMP001',
            department='HR',
            role='Manager',
            date_started='2023-01-01',
        )

    def test_talent_verify_admin_update_single_view(self):
        url = reverse('talent_verify_admin_update_single', kwargs={'employee_id': self.employee.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Update Employee Information')
        self.assertIsInstance(response.context['form'], EmployeeUpdateForm)

        # Test updating employee information
        updated_data = {
            'name': 'John Smith',
            'employee_id': 'EMP002',
            'department': 'Finance',
            'role': 'Accountant',
            'date_started': '2022-12-01',
            'date_left': '2023-06-30',
            'duties': 'Financial reporting',
        }
        response = self.client.post(url, data=updated_data)
        self.assertRedirects(response, reverse('employee_list'))

        # Check that the employee data has been updated in the database
        updated_employee = Employee.objects.get(id=self.employee.id)
        self.assertEqual(updated_employee.name, 'John Smith')
        self.assertEqual(updated_employee.employee_id, 'EMP002')
        self.assertEqual(updated_employee.department, 'Finance')
        self.assertEqual(updated_employee.role, 'Accountant')
        self.assertEqual(str(updated_employee.date_started), '2022-12-01')
        self.assertEqual(str(updated_employee.date_left), '2023-06-30')
        self.assertEqual(updated_employee.duties, 'Financial reporting')
