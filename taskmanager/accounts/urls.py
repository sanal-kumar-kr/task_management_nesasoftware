# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/delete/<uuid:id>/', views.delete_user, name='delete_user'),
    path('users/promote/<uuid:id>/', views.promote_to_admin, name='promote_user'),
    path('users/demote/<uuid:id>/', views.demote_to_user, name='demote_user'),
    path('assign-admin/', views.assign_admin_view, name='assign-admin'),
    path('user-admin-list/<uuid:uuid>/', views.user_admin_list_view, name='user-admin-list'),
    path('users/assign-role/<uuid:uuid>/', views.assign_role, name='assign_role'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/delete/<uuid:id>/', views.delete_task, name='delete_task'),
]
