"""file_upload URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from file_upload_app.views import render_home, play_song, list_all_files, delete_all_files, pause_current_music
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', include('file_upload_app.urls')),
    path(r'list_all/play_song/', play_song),
    path(r'play_song/', play_song),
    path(r'upload/play_song/', play_song),
    path('list_all/', list_all_files),
    path('delete_all/', delete_all_files),
    path('pause_current_music/', pause_current_music)
]
