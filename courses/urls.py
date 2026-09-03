from django.urls import path
from . import views


app_name = 'course'

urlpatterns = [
    
    #Course Url for Teacher or Instructor
    path('mine/', views.ManageCourseListView.as_view(), name='manage_course_list'),
    path('create/', views.CourseCreateView.as_view(), name='course_create'),
    path('edit/<int:pk>/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('delete/<int:pk>/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('<int:pk>/module/', views.CourseModuleUpdateView.as_view(), name='course_module_update'),
    
    #Course URL for Student 
    path('', views.CourseListView.as_view(), name='course_list'),
    path('subject/<slug:subject>', views.CourseListView.as_view(), name='course_list_subject'),
    path('detail/<slug:slug>', views.CourseDetailView.as_view(), name='course_detail'),
    
    
    #Content Url
    path('content/<int:module_id>/content/<str:model_name>/create/', views.ContentCreateUpdateView.as_view(), name='module_content_create'),
    path('content/<int:module_id>/content/<str:model_name>/update/<int:id>/', views.ContentCreateUpdateView.as_view(), name='module_content_update'),
    path('content/delete/<int:pk>', views.ContentDeleteView.as_view(), name='module_content_delete'),
    path('module/<int:module_id>/', views.ModuleContentListView.as_view(), name='module_content_list'),
    
    #Reordering 
    path('module/order/', views.ModuleOrderView.as_view(), name='module_order'),
    path('content/order/', views.ContentOrderView.as_view(), name='content_order'),
]
