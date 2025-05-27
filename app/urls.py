"""
URL configuration for askme project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('login/', views.login, name='login'),
    path('register/', views.signup, name='register'),
    path('settings/', views.settings_, name='settings'),
    path('user/logout/', views.logout, name='logout'),
    path('question/<int:question_id>/like_async/', views.like_async, name='like_async'),
    path('answer/<int:answer_id>/answer_like_async/', views.answer_like_async, name='answer_like_async'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)