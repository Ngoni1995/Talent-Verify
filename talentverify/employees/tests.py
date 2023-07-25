from django.test import TestCase
from django.urls import reverse
from .models import Employee, Company
from .forms import EmployeeUpdateForm, EmployeeBulkUpdateForm

class EmployeeUpdateTest(TestCase):
    def setUp(self):
        # Create a sample company
        self.company = Company.objects.create(
            name='Company ABC',
            date_of_registration='2023-01-01',
            company_registration_number='12345',
            address='123 Main Street',
            contact_person='John Smith',
            departments='HR, Finance',
            number_of_employees=100,
            contact_phone='123-456-7890',
            email_address='info@company.com',
        )

        # Create a sample employee belonging to the company
        self.employee = Employee.objects.create(
            company=self.company,
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
        # Create a sample company
        self.company = Company.objects.create(
            name='Company XYZ',
            date_of_registration='2023-01-01',
            company_registration_number='67890',
            address='456 Main Street',
            contact_person='Jane Doe',
            departments='IT, Marketing',
            number_of_employees=50,
            contact_phone='987-654-3210',
            email_address='info@companyxyz.com',
        )

        # Create a sample employee belonging to the company
        self.employee = Employee.objects.create(
            company=self.company,
            name='Jane Smith',
            employee_id='EMP003',
            department='IT',
            role='Developer',
            date_started='2022-12-01',
        )

    def test_talent_verify_admin_update_single_view(self):
        url = reverse('talent_verify_admin_update_single', kwargs={'employee_id': self.employee.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Update Employee Information')
        self.assertIsInstance(response.context['form'], EmployeeUpdateForm)

        # Test updating employee information
        updated_data = {
            'name': 'Jane Brown',
            'employee_id': 'EMP004',
            'department': 'Marketing',
            'role': 'Manager',
            'date_started': '2022-11-01',
            'date_left': '2023-07-31',
            'duties': 'Marketing strategy',
        }
        response = self.client.post(url, data=updated_data)
        self.assertRedirects(response, reverse('employee_list'))

        # Check that the employee data has been updated in the database
        updated_employee = Employee.objects.get(id=self.employee.id)
        self.assertEqual(updated_employee.name, 'Jane Brown')
        self.assertEqual(updated_employee.employee_id, 'EMP004')
        self.assertEqual(updated_employee.department, 'Marketing')
        self.assertEqual(updated_employee.role, 'Manager')
        self.assertEqual(str(updated_employee.date_started), '2022-11-01')
        self.assertEqual(str(updated_employee.date_left), '2023-07-31')
        self.assertEqual(updated_employee.duties, 'Marketing strategy')
