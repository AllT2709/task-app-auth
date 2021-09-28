from django.shortcuts import redirect, render
from django.views.generic import (
  ListView, 
  DetailView, 
  CreateView,
  UpdateView,
  DeleteView,
  FormView
  )
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth  import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import *
#from .forms import *

class CustomLoginView(LoginView):
  template_name='base/login.html'
  fields = '__all__'
  redirect_authenticated_user = True

  def get_success_url(self):
    return reverse_lazy('tasks')


class RegisterPage(FormView):
  model = Task
  form_class = UserCreationForm
  redirect_authenticated_user = True
  success_url = reverse_lazy('tasks')
  template_name = 'base/register.html'

  def form_valid(self, form):
    user = form.save()
    if user is not None:
      login(self.request,user)
    return super(RegisterPage,self).form_valid(form)

  def get(self, request, *args, **kwargs):
    if self.request.user.is_authenticated:
      return redirect('tasks')
    return super(RegisterPage,self).get(request, *args, **kwargs)

class TaskList(LoginRequiredMixin,ListView):
  model=Task
  context_object_name='tasks'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['tasks'] = context['tasks'].filter(user=self.request.user)
    context['count'] = context['tasks'].filter(complete=False).count()

    search_input = self.request.GET.get('search-area') or ''
    if search_input:
      context['tasks'] = context['tasks'].filter(title__startswith=search_input)
    
    context['search_input'] = search_input
    return context

class TaskDetail(LoginRequiredMixin,DetailView):
  model=Task

class TaskCreate(LoginRequiredMixin,CreateView):
  """ form_class=TaskForm
  template_name='base/task_form.html' """
  model=Task
  fields = ('title','description','complete')
  success_url = reverse_lazy('tasks')

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
  model=Task
  fields = ('title','description','complete')
  success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin,DeleteView):
  model = Task
  context_object_name='task'
  success_url = reverse_lazy('tasks')