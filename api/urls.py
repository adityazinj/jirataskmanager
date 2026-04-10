from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register),
    path('tasks/', get_tasks),
    path('tasks/create/', create_task),
    path('tasks/<int:id>/', update_task),
    path('tasks/<int:id>/delete/', delete_task),
    path('tasks/move/', move_task),
    path('dashboard/', dashboard),
    path('users/', get_users)
]