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
  teacher = Teacher.objects.filter(user=request.user)
  students = Child.objects.filter(teacher=request.user)
  print(teacher)
  return render(request,'teachers/index.html',{'teacher': teacher, 'students': students})

def guardians_index(request):
  guardians = Guardian.objects.all()
  return render(request,'guardians/index.html',{'guardians': guardians})

def guardians_detail(request, guardian_id):
  guardian = Guardian.objects.get(id=guardian_id)
  id_list = guardian.children.all().values_list('id')
  children_guardian_doesnt_have = Child.objects.exclude(id__in=id_list)
  return render(request, 'guardians/details.html', {
    'guardian': guardian,
    'children': children_guardian_doesnt_have
  })

def dashboard(request):
  user = request.user
  if hasattr(user, 'teacher'):
    return redirect('teachers_index')
  elif hasattr(user, 'guardian'):
     return redirect('guardians_detail', guardian_id=user.guardian.id)


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
              return redirect('guardians_detail', guardian_id=user.guardian.id)
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

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['guardians'] = self.object.guardian_set.all()
      return context


class ChildUpdate(UpdateView):
  model = Child
  fields = ['name', 'gender', 'DoB', 'allergies']

class ChildDelete(DeleteView):
  model = Child
  success_url = '/children'

def assoc_child(request, guardian_id, child_id):
  Guardian.objects.get(id=guardian_id).children.add(child_id)
  return redirect('guardians_detail', guardian_id=guardian_id)

def remove_child(request, guardian_id, child_id):
  Guardian.objects.get(id=guardian_id).children.remove(child_id)
  return redirect('guardians_detail', guardian_id=guardian_id)