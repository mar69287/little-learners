from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Teacher, Guardian, Child


# Create your views here.
def home(request):
  return render(request, 'home.html')

def teachers_index(request):
  teachers = Teacher.objects.filter(user=request.user)
  students = Child.objects.filter(teacher=request.user)
  print(teachers)
  return render(request,'teachers/index.html',{'teachers': teachers, 'students': students})

def guardians_index(request):
   guardians = Guardian.objects.all()
   print(guardians)
   return render(request,'guardians/index.html',{'guardians': guardians})

def guardians_detail(request, guardian_id):
  guardian = Guardian.objects.get(id=guardian_id)
  id_list = guardian.children.all().values_list('id')
  children_guarduan_doesnt_have = Child.objects.exclude(id__in=id_list)
  print(children_guarduan_doesnt_have)
  return render(request, 'guardians/details.html', {
    'guardian': guardian,
    'children': children_guarduan_doesnt_have
  })

def dashboard(request):
  user = request.user
  if hasattr(user, 'teacher'):
    return redirect('teachers_index')
  elif hasattr(user, 'guardian'):
    return redirect('guardians_index')


def login_view(request):
    error_message = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'teacher'):
              return redirect('teachers_index')
            elif hasattr(user, 'guardian'):
              return redirect('guardians_index')
        else:
            error_message = 'Invalid login - try again'
            return render(request, 'login.html')
            context = {'form': form, 'error_message': error_message}
    else:
        return render(request, 'login.html')

class ChildCreate(CreateView):
    model = Child
    fields = ['name', 'gender', 'DoB', 'allergies']

    def form_valid(self, form):
      form.instance.teacher = self.request.user
      return super().form_valid(form)

class ChildList(ListView):
  model = Child

class ChildDetail(DetailView):
  model = Child

class ChildUpdate(UpdateView):
  model = Child
  fields = ['name', 'gender', 'DoB', 'allergies']

class ChildDelete(DeleteView):
  model = Child
  success_url = '/children'

def assoc_child(request, cat_id, toy_id):
  Guardian.objects.get(id=guardian_id).children.add(child_id)
  return redirect('teachers_detail', guardian_id=guardian_id)

def remove_child(request, cat_id, toy_id):
  # Note that you can pass a toy's id instead of the whole toy object
  Cat.objects.get(id=guardian_id).toys.remove(child_id)
  return redirect('teachers_detail', guardian_id=guardian_id)
