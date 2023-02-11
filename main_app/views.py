from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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
  return render(request, 'guardians/details.html', {
    'guardian': guardian
  })

def dashboard(request):
  user = request.user
  if hasattr(user, 'teacher'):
    return redirect('teachers_index')
  elif hasattr(user, 'guardian'):
    return redirect('guardians_index')


class ChildCreate(CreateView):
  model = Child
  fields = ['name', 'DoB', 'gender', 'age']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

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

