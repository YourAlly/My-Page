from django.contrib import admin
from .models import Message, Post, Comment, Profile
# Register your models here.
admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Post)
admin.site.register(Comment)
