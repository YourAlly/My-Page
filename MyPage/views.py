from django.shortcuts import render, redirect
from MyPage.forms import RegistrationForm
from django.contrib import messages

from django.contrib.auth.models import User
from .models import Post, Comment, Message

# Create your views here.

def index(request):
    context = {
        'page_title': "Home",
        'posts': Post.objects.all()
    }
    return render(request, 'MyPage/index.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Registration Success!")
            return redirect('my-login')

    else:
        form = RegistrationForm()

    context = {
        'page_title': "Register",
        'form': form
    }
    return render(request, 'MyPage/register.html', context)


def profile(request):

    context = {
        'page_title': "My Profile",
    }
    return render(request, 'MyPage/profile.html', context)
