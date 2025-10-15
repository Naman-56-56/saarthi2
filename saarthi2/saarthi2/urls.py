"""
URL configuration for saarthi2 project.

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
from django.views.generic import TemplateView
from accounts import views as accounts_views
from dashboard import views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    
    # Home page
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
    
    # Accounts URLs
    path('signup/', accounts_views.signup, name='signup'),
    path('verify-otp/', accounts_views.verify_otp, name='verify_otp'),
    path('logout/', accounts_views.logout_view, name='logout'),
    
    # Dashboard URLs
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    path('dashboard/verify-apaar/', dashboard_views.verify_apaar, name='verify_apaar'),
]


