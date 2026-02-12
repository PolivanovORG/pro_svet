from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/relapse/<int:user_dependency_id>/', views.relapse_button_view, name='relapse_button'),
    path('dependency/<slug:slug>/', views.dependency_detail_view, name='dependency_detail'),
    path('dependency/<slug:slug>/not-having/', views.mark_dependency_not_having, name='mark_dependency_not_having'),
    path('dependency/<slug:slug>/assess/', views.assess_dependency_level, name='assess_dependency_level'),
    path('dependency/<slug:slug>/submit-assessment/', views.submit_assessment, name='submit_assessment'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),

    # Include authentication URLs for password reset, etc.
    path('accounts/', include('django.contrib.auth.urls')),
]