from django.urls import path
from .import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('<username>/', views.profile_view, name='userprofile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/delete/', views.profile_delete, name='profile_delete'),
    path('profile/onboarding/', views.profile_edit, name='profile-onboarding')
]
