from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailConfirmation
from django.http import Http404
from .forms import *

def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            return redirect_to_login(request.get_full_path())
    return render(request, 'monkeyusers/profile.html', {'profile':profile})


@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)  
    
    # Check if this is onboarding (from email verification)
    onboarding = request.GET.get('onboarding', False)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            # If this was onboarding, redirect to home, otherwise go back to profile
            if onboarding:
                messages.success(request, "Welcome to Monkey Snowfight! Your profile is all set up!")
                return redirect('home')
            else:
                return redirect('profile')
        
    # Also check the path for existing onboarding logic
    if request.path == reverse('profile-onboarding'):
        onboarding = True
      
    return render(request, 'monkeyusers/profile_edit.html', { 'form':form, 'onboarding':onboarding })


@login_required
def profile_settings_view(request):
    return render(request, 'monkeyusers/profile_settings.html')


@login_required
def profile_emailchange(request):
    
    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'partials/email_form.html', {'form':form})
    
    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)

        if form.is_valid():
            
            # Check if the email already exists
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already in use.')
                return redirect('profile-settings')
            
            form.save() 
            
            # Then Signal updates emailaddress and set verified to False
            
            # Then send confirmation email 
            # send_email_confirmation() will be deprecated soon!
            send_email_confirmation(request, request.user)
            
            return redirect('profile-settings')
        else:
            messages.warning(request, 'Email not valid or already in use')
            return redirect('profile-settings')
        
    return redirect('profile-settings')


@login_required
def profile_usernamechange(request):
    if request.htmx:
        form = UsernameForm(instance=request.user)
        return render(request, 'partials/username_form.html', {'form':form})
    
    if request.method == 'POST':
        form = UsernameForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Username updated successfully.')
            return redirect('profile-settings')
        else:
            messages.warning(request, 'Username not valid or already in use')
            return redirect('profile-settings')
    
    return redirect('profile-settings')    


@login_required
def profile_emailverify(request):
    send_email_confirmation(request, request.user)
    return redirect('profile-settings')


@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, what a pity')
        return redirect('home')
    
    return render(request, 'monkeyusers/profile_delete.html')


class CustomConfirmEmailView(ConfirmEmailView):
    """Custom email confirmation view that ensures user gets logged in"""
    
    def post(self, *args, **kwargs):
        try:
            self.object = self.get_object()
            # Get the user from the email confirmation
            user = self.object.email_address.user
            
            # Confirm the email
            self.object.confirm(self.request)
            
            # Log in the user
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # Add success message
            messages.success(self.request, f"Welcome {user.username}! Your email has been verified.")
            
            # Redirect to profile edit with onboarding
            return redirect('/profile/edit/?onboarding=true')
            
        except Exception as e:
            messages.error(self.request, "There was an error confirming your email.")
            return redirect('account_login')
    
    def get(self, *args, **kwargs):
        # For GET requests, do the same as POST
        return self.post(*args, **kwargs)
