from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("teachers/", views.teachers_index, name='teachers_index'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('guardians/',views.guardians_index, name ='guardians_index'),
    path('guardians/<int:guardian_id>/', views.guardians_detail, name='guardians_detail'),
    path('children/create/', views.ChildCreate.as_view(), name='children_create'),
]