from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'default_avatar', 'displayname', 'info' ]
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form__input form__input--file'}),
            'default_avatar': forms.HiddenInput(),  # Hidden field for JavaScript to update
            'displayname' : forms.TextInput(attrs={'placeholder': 'Add display name', 'class': 'form__input'}),
            'info' : forms.Textarea(attrs={'rows':3, 'placeholder': 'Add information', 'class': 'form__input form__textarea'})
        }
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        
        # Check what's happening with the fields
        has_new_image = bool(self.files.get('image'))
        has_default_avatar = bool(profile.default_avatar)
        
        # If a default avatar is selected and no new image was uploaded
        if has_default_avatar and not has_new_image:
            profile.image = None
        # If a new image is uploaded, clear the default avatar selection
        elif has_new_image:
            profile.default_avatar = ''
        
        if commit:
            profile.save()
        return profile
        
        
class EmailForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']


class UsernameForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']
