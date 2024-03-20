from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm
from django.contrib.auth import logout
from django.http  import Http404
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else: 
        try:
            profile = request.user.profile
        except:
            raise Http404()
    return render(request, 'users/profile.html', {'profile':profile})

@login_required
def profile_edit(request):
    form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,  instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('profile')
        
    if request.path == reverse('profile-onboarding'):
        template = 'users/profile_onboarding.html'
    else:
        template = 'users/profile_edit.html'
    
    return render(request, template, {'form':form})

@login_required
def profile_delete(request):
    user = request.user
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, Ayaah so sorry Koh!')
        return redirect('home')
    return render(request, 'users/profile_delete.html')
