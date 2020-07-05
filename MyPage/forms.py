from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Comment, Post
from django import forms

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'special'}), max_length=256)


class PostForm(forms.Form):
    title = forms.CharField(max_length=32, label="Title")
    content = forms.CharField(widget=forms.Textarea, max_length=512)

