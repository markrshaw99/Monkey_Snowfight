from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib import messages
from allauth.account.signals import user_signed_up

@receiver(post_save, sender=User)       
def user_postsave(sender, instance, created, **kwargs):
    user = instance
    
    # add profile if user is created
    if created:
        Profile.objects.create(
            user = user,
        )
    else:
        # update allauth emailaddress if exists 
        try:
            email_address = EmailAddress.objects.get_primary(user)
            if email_address.email != user.email:
                email_address.email = user.email
                email_address.verified = False
                email_address.save()
        except:
            # if allauth emailaddress doesn't exist create one
            EmailAddress.objects.create(
                user = user,
                email = user.email, 
                primary = True,
                verified = False
            )
        
        
@receiver(pre_save, sender=User)
def user_presave(sender, instance, **kwargs):
    if instance.username:
        instance.username = instance.username.lower()

# Try both Django and allauth signals
@receiver(user_logged_in)
def django_login_message(sender, request, user, **kwargs):
    messages.success(request, f"Welcome back, {user.profile.name}!")

@receiver(user_logged_out)
def django_logout_message(sender, request, user, **kwargs):
    if user:
        messages.info(request, "You have been logged out successfully.")        