from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

app_name = 'student'

urlpatterns = [
    #Register user 
    path('', views.home, name='home'),
    path('register/', views.StudentRegistrationView.as_view(), name='student_registration'),
    path('enroll-course/', views.StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    
    #Course list 
    path('course', views.StudentCourseListView.as_view(), name='student_course_list'),
    
    #Module list
    # path('course/<int:pk>', cache_page(60 * 15)(views.StudentCourseDetailView.as_view()), name='student_course_detail'),
    path('course/<int:pk>', views.StudentCourseDetailView.as_view(), name='student_course_detail'),
    path('course/<int:pk>/<int:module_id>', cache_page(60 * 15)(views.StudentCourseDetailView.as_view()), name='student_course_detail_module'),    
    
    #Become a teacher
    path('request-teacher/', views.request_teacher, name='request_teacher'),
]
