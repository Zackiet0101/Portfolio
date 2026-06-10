from django.urls import path
from . import views

app_name = 'portfolio_app'

urlpatterns = [
    path('', views.front, name='front'),
    path('front/', views.profile, name='profile'),
    path('skills/', views.skill_ielts, name='skill_ielts'),
    path('projects/', views.project_list, name='project_list'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
]

