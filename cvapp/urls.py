from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employee/create/', views.employee_create, name='employee_create'),
    path('employee/<int:pk>/upload/', views.upload_cv, name='employee_upload'),
]
