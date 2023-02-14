from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from datetime import date
from django.urls import reverse_lazy
from .forms import CommentForm
from .models import Teacher, Guardian, Child, Attendance, Assessment, Feeding, Comment



def home(request):
  return render(request, 'home.html')

@login_required
def teachers_index(request):
  user = request.user
  if hasattr(user, 'teacher'):
    teacher = Teacher.objects.filter(user=request.user)
    students = Child.objects.filter(teacher=request.user)
    today = date.today()

    for student in students:
          attendance_today = student.attendance_set.filter(date=today)
          student.attendance_today = attendance_today.exists()
          assessment_today = student.assessment_set.filter(date=today)
          student.assessment_today = assessment_today.exists()

    return render(request, 'teachers/index.html', {'teacher': teacher, 'students': students})
  else:
    return redirect('dashboard')

@login_required
def guardians_index(request):
  user = request.user
  if hasattr(user, 'teacher'):
    guardians = Guardian.objects.all()
    return render(request,'guardians/index.html',{'guardians': guardians})
  else:
    return redirect('dashboard')

@login_required
def guardians_detail(request, guardian_id):
    guardian = Guardian.objects.get(id=guardian_id)
    id_list = guardian.children.all().values_list('id')
    children_guardian_doesnt_have = Child.objects.exclude(id__in=id_list)
    return render(request, 'guardians/details.html', {
      'guardian': guardian,
      'children': children_guardian_doesnt_have
    })


@login_required
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

class ChildCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Child
    fields = ['name', 'gender', 'DoB', 'allergies']
    permission_required = "main_app.is_teacher"
    
    def form_valid(self, form):
      form.instance.teacher = self.request.user
      return super().form_valid(form)

    def handle_no_permission(self):
        return redirect('dashboard')

class ChildList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
  model = Child
  permission_required = "main_app.is_teacher"

  def handle_no_permission(self):
        return redirect('dashboard')

class ChildDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Child
    permission_required = "main_app.is_teacher"

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['guardians'] = self.object.guardian_set.all()
      context['attendance'] = Attendance.objects.filter(child=self.object)
      context['assessment'] = Assessment.objects.filter(child=self.object)
      context['feeding'] = Feeding.objects.filter(child=self.object)
      context['comment_form'] = CommentForm()
      return context
    
    def handle_no_permission(self):
        return redirect('dashboard')

class ChildUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
  model = Child
  fields = ['name', 'gender', 'DoB', 'allergies']
  permission_required = "main_app.is_teacher"

  def handle_no_permission(self):
        return redirect('dashboard')

class ChildDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
  model = Child
  success_url = '/children'
  permission_required = "main_app.is_teacher"

  def handle_no_permission(self):
        return redirect('dashboard')

@login_required
def assoc_child(request, guardian_id, child_id):
  user = request.user
  if hasattr(user, 'teacher'):
    Guardian.objects.get(id=guardian_id).children.add(child_id)
    return redirect('guardians_detail', guardian_id=guardian_id)
  else:
    return redirect('dashboard')
  

@login_required
def remove_child(request, guardian_id, child_id):
  user = request.user
  if hasattr(user, 'teacher'):
    Guardian.objects.get(id=guardian_id).children.remove(child_id)
    return redirect('guardians_detail', guardian_id=guardian_id)
  else:
    return redirect('dashboard')

@login_required
def add_comment(request, child_id):
  user = request.user
  if hasattr(user, 'teacher'):
    if request.method == 'POST':
      form = CommentForm(request.POST)
      if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.child_id = child_id
        new_comment.save()
    return redirect('children_detail', pk=child_id)
  else:
    return redirect('dashboard')

@login_required
def comment_delete(request, pk):
  user = request.user
  if hasattr(user, 'teacher'):
    comment = Comment.objects.get(pk=pk)
    child_id = comment.child.id
    comment.delete()
    return redirect('children_detail', pk=child_id)
  else:
    return redirect('dashboard')
  

@login_required
def attendance(request, child_id, status):
  user = request.user
  if hasattr(user, 'teacher'):
    child = Child.objects.get(id=child_id)
    attendance = Attendance(child=child, status=status)
    attendance.save()
    return redirect('teachers_index')
  else:
    return redirect('dashboard')
  
  
@login_required
def assessments(request):
  user = request.user
  if hasattr(user, 'teacher'):
    teacher = Teacher.objects.filter(user=request.user)
    students = Child.objects.filter(teacher=request.user)
    today = date.today()
    return render(request, 'assessments/index.html', {'teacher': teacher, 'students': students})
  else:
    return redirect('dashboard')

class AttendanceDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
  model = Attendance
  success_url = reverse_lazy('children_list')
  permission_required = "main_app.is_teacher"

  def get_success_url(self):
    return reverse_lazy('children_detail', kwargs={'pk': self.object.child.id})

  def handle_no_permission(self):
        return redirect('dashboard')
  
@login_required
def assessment_create(request, child_id, behavior):
  user = request.user
  if hasattr(user, 'teacher'):
    child = Child.objects.get(id=child_id)
    assessment = Assessment(child=child, behavior=behavior)
    assessment.save()
    return redirect('teachers_index')
  else:
    return redirect('dashboard')

class AssessmentDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
  model = Assessment
  success_url = reverse_lazy('children_list')
  permission_required = "main_app.is_teacher"

  def get_success_url(self):
    return reverse_lazy('children_detail', kwargs={'pk': self.object.child.id})

  def handle_no_permission(self):
        return redirect('dashboard')

@login_required
def feeding_create(request, child_id, did_eat):
  user = request.user
  if hasattr(user, 'teacher'):
    child = Child.objects.get(id=child_id)
    feeding = Feeding(child=child, did_eat=did_eat)
    feeding.save()
    return redirect('teachers_index')
  else:
    return redirect('dashboard')

class FeedingDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
  model = Feeding
  success_url = reverse_lazy('children_list')
  permission_required = "main_app.is_teacher"

  def get_success_url(self):
    return reverse_lazy('children_detail', kwargs={'pk': self.object.child.id})

  def handle_no_permission(self):
        return redirect('dashboard')
    