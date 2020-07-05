from django.shortcuts import render, redirect
from itertools import chain
from MyPage import forms
from .models import Post, Comment, Message
from django.contrib import messages
from django.http import JsonResponse

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView


# Create your views here.

class LoginView(auth_views.LoginView):
    template_name = "MyPage/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Login'
        return context


class PostsView(ListView):
    model = Post
    template_name = 'MyPage/index.html'
    context_object_name = 'posts'
    ordering = ['-time_posted']
    paginate_by = 6
    

# User profile page
def user(request, user_id):
    target = User.objects.get(pk=user_id)
    posts = Post.objects.filter(author=target).order_by('-time_posted')
    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 5)
    try:
        user_posts = paginator.page(page)
    except PageNotAnInteger:
        user_posts = paginator.page(1)
    except EmptyPage:
        user_posts = paginator.page(paginator.num_pages)

    context = {
        'page_title': "My Profile",
        'target': target,
        'posts': user_posts
    }
    return render(request, 'MyPage/profile.html', context)


def post(request, post_id):
    target = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(on_post=target).order_by('-time_commented')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 5)
    try:
        post_comments = paginator.page(page)
    except PageNotAnInteger:
        post_comments = paginator.page(1)
    except EmptyPage:
        post_comments = paginator.page(paginator.num_pages)

    context = {
        'page_title': "My Profile",
        'post': target,
        'comments': post_comments,
        'form': forms.CommentForm()
    }
    return render(request, 'MyPage/post.html', context)


# Registers a user
def register(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Registration Success!")
            return redirect('my-login')

    else:
        form = forms.RegistrationForm()

    context = {
        'page_title': "Register",
        'form': form
    }
    return render(request, 'MyPage/form.html', context)


@login_required
def post_form(request):
    if request.method == 'POST':
        form = forms.PostForm(request.POST)
        if form.is_valid():
            new_post = Post(author=request.user,
            title=form.cleaned_data['title'],
            content=form.cleaned_data['content'] if not form.cleaned_data['content'] == '' else None)
            new_post.save()
            messages.success(request, "Post Created")
            return redirect('my-index')
    else:
        form = forms.PostForm(initial={'title': ''})
    context = {
        'page_title': "Post",
        'form': form
    }
    return render(request, 'MyPage/form.html', context)

@login_required
def send_message(request, target_id):
    if request.method == 'POST':
        form = forms.MessageForm(request.POST)
        if form.is_valid():
            new_message = Message(sent_by=request.user,
                            sent_to=User.objects.get(pk=target_id),
                            title=form.cleaned_data['title'],
                            message=form.cleaned_data['content'] if not form.cleaned_data['content'] == '' else None)
            new_message.save()
            messages.success(request, "Message Sent")
            return redirect('my-user', target_id)
    else:
        form = forms.MessageForm(initial={'title': ''})
    context = {
        'page_title': "Send Message",
        'form': form
    }
    return render(request, 'MyPage/form.html', context)


@login_required
def process_comment(request, post_id):
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            new_comment = Comment(commenter=request.user,
                                  on_post=Post.objects.get(pk=post_id),
                                  comment=form.cleaned_data['comment'])
            new_comment.save()
            messages.success(request, "Comment Posted!")
    else:
        messages.error(request, "Something went wrong")

    return redirect('my-post', post_id)

@login_required
def contacts(request):

    context = {
        'page_title': "Contacts"
    }
    return render(request, 'MyPage/contacts.html', context)


@login_required
def update_image(request):
    if request.method == 'POST':
        form = forms.ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('my-user', request.user.id)
    else:
        form = forms.ProfileUpdateForm()

    context = {
        'page_title': "Change Profile Picture",
        'form': form,
        'multipart': True
    }
    return render(request, 'MyPage/form.html', context)


@login_required
def update_email(request):
    if request.method == 'POST':
        form = forms.UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('my-user', request.user.id)
    else:
        form = forms.UserUpdateForm()

    context = {
        'page_title': "Update Email",
        'form': form
    }
    return render(request, 'MyPage/form.html', context)


@login_required
def add(request, user_id):
    user1 = User.objects.get(pk=user_id)
    request.user.profile.contacts.add(user1)
    messages.success(request, f"{user1.username} added to contacts")
    return redirect("my-user", user_id=user_id)


@login_required
def remove(request, user_id):
    user1 = User.objects.get(pk=user_id)
    request.user.profile.contacts.remove(user1)
    messages.success(request, f"{user1.username} removed from contacts")
    return redirect("my-user", user_id=user_id)


@login_required
def chat(request, target_id):
    target = User.objects.get(pk=target_id)
    target_messages = Message.objects.filter(sent_by=target, sent_to=request.user)
    user_messages = Message.objects.filter(sent_by=request.user, sent_to=target)
    all_messages = target_messages|user_messages
    all_messages = all_messages.order_by('-time_sent')

    context ={
        'page_title': "Chat",
        'sent_messages': all_messages,
        'target': target
    }

    return render(request, 'MyPage/chat.html', context)

@login_required
def chat_send(request, target_id):
    target = User.objects.get(pk=target_id)
    message = request.POST.get('message')
    new_message = Message(sent_by=request.user, sent_to=target, message=message)

    new_message.save()

    return JsonResponse({'success': True, 'error': None})


@login_required
def chat_get(request, target_id):
    target = User.objects.get(pk=target_id)
    target_messages = Message.objects.filter(
        sent_by=target, sent_to=request.user)
    user_messages = Message.objects.filter(
        sent_by=request.user, sent_to=target)
    all_messages = target_messages|user_messages
    all_messages = all_messages.order_by('-time_sent')[:20]

    messages = []
    for data in all_messages:
        message = {'sent_by': data.sent_by.username,
                    'sent_by_id': data.sent_by.id,
                    'sent_by_image': data.sent_by.profile.image.url,
                    'sent_to': data.sent_to.username,
                    'sent_to_id': data.sent_to.id,
                    'sent_to_image': data.sent_to.profile.image.url,
                    'message': data.message,
                    'time_sent': data.time_sent.strftime("%x %X")
                    }

        messages.append(message)

    return JsonResponse({'sent_messages': messages})

def user_search(request):
    all_users = User.objects.exclude(pk=request.user.id)
    page = request.GET.get('page', 1)
    paginator = Paginator(all_users, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {
        'page_title': "Search",
        'searched_users': users
    }
    
    return render(request, "MyPage/search.html", context)
