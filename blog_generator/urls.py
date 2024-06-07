from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('generate-blog', views.generate_blog, name='generate-blog'),
    path('qualitylink', views.qualitylink, name='qualitylink')
]
    