from django.forms import ModelForm
from django import forms
from .models import *

class ChatMessageCreateForm(ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Add a message...', 'class': 'form__input', 'maxlength' : '300', 'autofocus': True}),
        }
    
    def clean_body(self):
        body = self.cleaned_data.get('body')
        if not body or not body.strip():
            raise forms.ValidationError("Message cannot be empty.")
        return body.strip()


class NewGroupForm(ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name': forms.TextInput(attrs={
                'placeholder': 'Add name ...',
                'class': 'form__input',
                'maxlength': '300',
                'autofocus': True
                }),
        }

class ChatRoomEditForm(ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name': forms.TextInput(attrs={
                'placeholder': 'Edit chat name ...',
                'class': 'form__input',
                'maxlength': '300',
            }),
        }