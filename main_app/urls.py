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
    path('guardians/<int:guardian_id>/assoc_child/<int:child_id>/', views.assoc_child, name='assoc_child'),
    path('guardians/<int:guardian_id>/remove_child/<int:child_id>/', views.remove_child, name='remove_child'),
    path('children/create/', views.ChildCreate.as_view(), name='children_create'),
    path('children/', views.ChildList.as_view(), name='children_index'),
    path('children/<int:pk>/', views.ChildDetail.as_view(), name='children_detail'),
    path('children/<int:pk>/update/', views.ChildUpdate.as_view(), name='children_update'),
    path('children/<int:pk>/delete/', views.ChildDelete.as_view(), name='children_delete'),
    path('attendance/<int:pk>/delete/', views.AttendanceDelete.as_view(), name='attendance_delete'),
    path('attendance/<int:child_id>/<str:status>/', views.attendance, name='attendance'),
    #path("assessments/", views.assessments_index, name='assessments_index'),
    path('assessments/<int:pk>/delete/', views.AssessmentDelete.as_view(), name='assessment_delete'),
    path('assessments/<int:child_id>/<str:behavior>/', views.assessment_create, name='assessment_create'),
]