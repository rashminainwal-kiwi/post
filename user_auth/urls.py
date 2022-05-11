from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register.as_view(), name='register'),
    path('login', views.login.as_view(), name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout.as_view(), name='logout'),
    path('activate/<uidb64>/<token>', views.Activate.as_view(), name='activate'),
]
