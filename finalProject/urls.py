"""
URL configuration for finalProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from service import views
from service.views import CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetView, \
    CustomPasswordResetCompleteView

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('admin/', admin.site.urls),
    path('chat/', views.chat, name='chat'),
    path('demo/', views.demo, name='demo'),
    path('', views.advert, name='advert'),
    path('register/', views.register, name='register'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='reset_password'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/complete', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('clear_chat/', views.clear_chat, name='clear_chat'),

]
