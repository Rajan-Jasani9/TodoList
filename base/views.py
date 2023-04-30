from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView , DeleteView, UpdateView 
from django.urls import reverse_lazy

from django.views.decorators.cache import never_cache
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout

from .models import task
# Create your views here.


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks') 
    
    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        
        return super(RegisterPage,self).form_valid(form)
    # def get(self, *args, **kwargs):
    #     if self.request.user.is_authenticate:
    #         return redirect('tasks')
    #     return super(RegisterPage,self).get()
        
# @never_cache
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')

  


# class TaskList(LoginRequiredMixin,ListView):
#     model = task
#     context_object_name =  'tasks'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["tasks"] = context["tasks"].filter(user=self.request.user)
#         context["count"] = context["tasks"].filter(complete=False)
        
#         search_input = self.request.GET.get('Search-area') or ''
#         if search_input:
#             context["tasks"] = context["tasks"].filter(title__icontains = search_input  )
        
#         context['search_input'] = search_input
        
#         return context
    
    
class TaskList(LoginRequiredMixin, ListView):
    model = task
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        queryset = queryset.filter(complete=False)
        search_input = self.request.GET.get('Search-area') or ''
        if search_input:
            queryset = queryset.filter(title__icontains=search_input)
        return queryset


    
    
class TaskDetail(LoginRequiredMixin,DetailView):
    model = task
    
class TaskCreate(LoginRequiredMixin,CreateView):
    model = task
    fields = ["title", 'description', 'complete']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = task
    fields = ["title", 'description', 'complete']
    success_url = reverse_lazy('tasks')
    
class TaskDelete(LoginRequiredMixin,DeleteView):
    model = task
    context_object_name = "task"
    success_url = reverse_lazy('tasks')
    
@never_cache
def logout_view(request):
    logout(request)
    return redirect('login')