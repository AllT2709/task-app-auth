from django.urls import path
from django.contrib.auth.views import LogoutView


from .views import *

urlpatterns = [
  path('register/',RegisterPage.as_view(), name='register'),
  path('login/',CustomLoginView.as_view(), name='login'),
  path('logut/',LogoutView.as_view(next_page='login'), name='logout'),
  path('',TaskList.as_view(), name='tasks'),
  path('task/<int:pk>',TaskDetail.as_view(), name='detail'),
  path('create-task/',TaskCreate.as_view(), name='create'),
  path('update-task/<int:pk>',TaskUpdate.as_view(), name='update'),
  path('delete-task/<int:pk>',TaskDelete.as_view(), name='delete'),
]