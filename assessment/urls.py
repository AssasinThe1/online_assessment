from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home page and authentication URLs
    path('sign_in/', views.sign_in, name='sign_in'),  # Sign-in view
    path('register/', views.register, name='register'),  # Registration view
    # Test-taking URLs
    path('test/', views.test, name='test'),  # Test page where users answer questions
    path('submit/', views.submit, name='submit'),  # Submission of the test
    path('results/', views.results, name='results'),  # Results after submitting the test
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('time_expired/', views.time_expired, name='time_expired'),
    path('', views.home, name='home'),
    path('test/<int:test_type_id>/', views.test, name='test'),
]
