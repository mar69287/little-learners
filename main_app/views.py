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

  return render(request, 'teachers/index.html', {'teachers': teachers, 'students': students})

def guardians_index(request):
   guardians = Guardian.objects.all()
   print(guardians)
   return render(request,'guardians/index.html',{'guardians': guardians})

def guardians_detail(request, guardian_id):
  guardian = Guardian.objects.get(id=guardian_id)
  id_list = guardian.toys.all().values_list('id')
  print(id_list)
  return render(request, 'guardians/detail.html', {
    'guardian': guardian
  })

class ChildCreate(CreateView):
  model = Child
  fields = ['name', 'DoB', 'gender', 'age']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
def login_view(request):
    error_message = ''
    if request.method == 'POST':
        print("i have reached post method of login")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print("i am in user is not none")
            if hasattr(user, 'teacher'):
              print("i am a teacher")
              return redirect('teachers_index')
            elif hasattr(user, 'guardian'):
              print("i am a guardian")
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

