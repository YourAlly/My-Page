from django.shortcuts import render, redirect
from MyPage.forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm, CommentForm, PostForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment, Message

from django.views.generic import ListView, DetailView, CreateView

# Create your views here.

# Views all posts
class PostsView(ListView):
    model = Post
    template_name = 'MyPage/index.html'
    context_object_name = 'posts'
    ordering = ['-time_posted']


# Views a certain post with comments
class PostDetailView(DetailView):
    model = Post
    template_name = 'MyPage/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm
        return context


# Views a certain amount of posts
def index(request):
    context = {
        'page_title': "Home",
        'posts': Post.objects.all().order_by('-time_posted')[:10]
    }
    return render(request, 'MyPage/index.html', context)

# Registers a user
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
def post_form(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():

            new_post = Post(author=request.user,
            title=form.cleaned_data['title'],
            content=form.cleaned_data['content'] if not form.cleaned_data['content'] == '' else None)
            new_post.save()
            messages.success(request, "Post Created")
            return redirect('my-index')
    else:
        form = PostForm()
    context = {
        'page_title': "Post",
        'form': form
    }
    return render(request, 'MyPage/form.html', context)


@login_required
def process_comment(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = Comment(commenter=request.user,
                                  on_post=Post.objects.get(pk=post_id),
                                  content=form.cleaned_data['comment'])
            new_comment.save()
            messages.success(request, "Comment Posted!")
    else:
        messages.error(request, "Something went wrong")

    return redirect('my-post', post_id)

# User profile page
@login_required
def user(request, user_id):

    context = {
        'page_title': "My Profile",
        'target': User.objects.get(pk=user_id)
    }
    return render(request, 'MyPage/profile.html', context)


@login_required
def contacts(request):

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
