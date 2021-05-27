from django.urls import path

from . import views
from users import views as user_views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

app_name = 'roommate_app'
urlpatterns = [
    #path('index/', TemplateView.as_view(template_name='index.html'), name='index'),
    path('index/', user_views.loadMainPage, name='index'),
    path('logout', LogoutView.as_view(), name='logout'),
    #path('home/', user_views.home, name='home')
    #path('profile/', views.edit_profile, name='profile')
]