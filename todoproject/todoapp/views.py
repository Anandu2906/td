from django.shortcuts import render, redirect
from .models import Task
from . forms import TodoForm

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView,DeleteView

#Class Based Views.
class TaskListView(ListView):
    model = Task                   #modelname
    template_name = 'home.html'    #template name
    context_object_name = 'tasks'  #variable name

class TaskDetailView(DetailView):
    model = Task
    template_name = 'detail.html'
    context_object_name = 'task'

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'update_cbv.html'
    context_object_name = 'task'
    fields = ('name', 'priority', 'date')    #the fields we want to edit
    def get_success_url(self):     #the URL to redirect to when the form is successfully validated.
        return reverse_lazy('todoapp:cbvdetail', kwargs={'pk': self.object.id})

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('todoapp:cbvhome')

#Function Based Views.
def add(request):
    tasks = Task.objects.all()  # calling all the task objects to display in home.html
    if request.method == 'POST':
        #saving task and priority
        name = request.POST.get('task', '')
        priority = request.POST.get('priority', '')
        date = request.POST.get('date', '')
        task = Task(name=name, priority=priority, date=date)
        task.save()
    return render(request, 'home.html', {'tasks': tasks})

def delete(request,taskid):
    task = Task.objects.get(id=taskid)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request, 'delete.html')

def update(request,id):
    task = Task.objects.get(id=id)
    f = TodoForm(request.POST or None, instance=task)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request, 'update.html', {'f': f, 'task': task})

