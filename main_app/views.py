from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Teacher, Guardian


# Create your views here.
def home(request):
  return render(request, 'home.html')

def teachers_index(request):
  teachers = Teacher.objects.filter(user=request.user)
  print(teachers)

  return render(request, 'teachers/index.html', {'teachers': teachers})

def guardians_index(request):
   guardians = Guardian.objects.filter(user=request.user)
   print(guardians)
   return render(request,'guardians/index.html',{'guardians': guardians})

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