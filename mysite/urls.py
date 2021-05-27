"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from users import views as user_views
from . import views

urlpatterns = [
    path('', include('roommate_app.urls')),
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('profile/', user_views.profile, name='profile'),
    path('friends/', user_views.loadFriendPage, name='friends'),
    path('friend_requests/', user_views.loadFriendRequests, name='friend requests'),
    path('send_roommate_request/<int:userID>/', user_views.send_roommate_request, name='send roommate request'),
    path('accept_roommate_request/<int:requestID>/', user_views.accept_roommate_request, name='accept roommate request'),
    path('search_profiles/', user_views.searching, name='search roommate'),
    path('search_all_profiles/', user_views.searchingAll, name='search all roommates'),
    path('view_profile/<int:userID>/', user_views.view_profile, name='view_profile'),
    path('preferences/', user_views.preferences, name='preferences'),
    path('chat/', user_views.chat, name='chat'),
    path('chat/<int:userID>/', user_views.chat, name='chat'),
    path('chat/callback', user_views.chat_callback, name='chat_callback'),
    path('chat_send/', user_views.chat_send, name='chat_send'),
    path('chat_send/<int:userID>/', user_views.chat_send, name='chat_send'),
    path('post/new/', user_views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', user_views.PostDetailView.as_view(), name='post-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

