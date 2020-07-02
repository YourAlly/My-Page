from django.shortcuts import render, redirect
from MyPage.forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment, Message

# Create your views here.

def index(request):
    context = {
        'page_title': "Home",
        'posts': Post.objects.all().order_by('-time_posted')[:10]
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
    return render(request, 'MyPage/form.html', context)

@login_required
def user(request, user_id):

    context = {
        'page_title': "My Profile",
        'target': User.objects.get(pk=user_id)
    }
    return render(request, 'MyPage/profile.html', context)

@login_required
def messenger(request):

    context = {
        'page_title': "Contacts"
    }
    return render(request, 'MyPage/contacts.html', context)

@login_required
def update_image(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('my-user', request.user.id)
    else:
        form = ProfileUpdateForm()

    context = {
        'page_title': "Change Profile Picture",
        'form': form,
        'multipart': True
    }
    return render(request, 'MyPage/form.html', context)


@login_required
def update_email(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('my-user', request.user.id)
    else:
        form = UserUpdateForm()

    context = {
        'page_title': "Update Email",
        'form': form
    }
    return render(request, 'MyPage/form.html', context)

@login_required
def add(request, user_id):
    user1 = User.objects.get(pk=user_id)
    request.user.profile.friends.add(user1)
    messages.success(request, f"{user1.username} added to contacts")
    return redirect("my-user", user_id=user_id)


@login_required
def remove(request, user_id):
    user1 = User.objects.get(pk=user_id)
    request.user.profile.friends.remove(user1)
    messages.success(request, f"{user1.username} removed from contacts")
    return redirect("my-user", user_id=user_id)
