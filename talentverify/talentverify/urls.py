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
    path('employee/<int:employee_id>/update/', views.employee_update, name='employee_update'),
    path('employee/list/', views.employee_list, name='employee_list'),  # URL pattern for employee list view
]

# Include router.urls at the end of urlpatterns
urlpatterns += router.urls
