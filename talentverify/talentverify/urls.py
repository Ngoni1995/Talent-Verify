from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from employees.views import EmployeeViewSet
from employees import views

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

app_name = 'employees'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   
    path('employee/list/', views.employee_list, name='employee_list'),  # URL pattern for employee list view

      # Add the URL pattern for bulk update view
    path('bulk_update/', views.bulk_update_employees, name='bulk_update_employees'),

    # Updated URL pattern for single-entry update view without employee_id
    path('employee/update_single/', views.employee_update_single, name='employee_update_single'),
    # Keep the existing URL pattern for employee_update view
    path('employee/<int:employee_id>/update/', views.employee_update, name='employee_update'),

    path('employee/talent_verify_admin/update_single/<int:employee_id>/', views.talent_verify_admin_update_single, name='talent_verify_admin_update_single'),
    path('employee/talent_verify_admin/bulk_update/', views.talent_verify_admin_bulk_update, name='talent_verify_admin_bulk_update'), 

]

# Include router.urls at the end of urlpatterns
urlpatterns += router.urls
