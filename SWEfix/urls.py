"""
URL configuration for SWE project.

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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.views import AuthViewSet
from application import views
from application.views import submit_application

router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewSet, basename='auth')


urlpatterns = [ 
    path('admin/', admin.site.urls),  # This line includes the admin URLs
    path('', include(router.urls)),  # Include your existing URLs
    path('submit/', views.submit_application, name='submit_application'),
    path('get_applications/', views.get_applications, name='get_applications'),
    path('review/<int:applicant_id>/', views.review_form, name='review_form'),
    path('pending-applications/', views.pending_applications, name='pending_applications'),
    path('applicants/<int:applicant_id>/', views.applicant_with_appointment, name='applicant_with_appointment'),
    path('pending-appointment/', views.pending_appointment, name='pending_appointment'),
]
