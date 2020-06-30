from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="written_posts")
    time_posted = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    def __str__(self):
        return f"{author}: {time_posted}"


class Comment(models.Model):
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="written_comments")
    on_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments")
    time_commented = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    def __str__(self):
        return f"{commenter}: {time_commented}"


class Message(models.Model):
    by = models.ForeignKey(User, on_delete=models.CASCADE,
                           related_name='sent_messages')
    to = models.ForeignKey(User, on_delete=models.CASCADE,
                           related_name='recieved_messages')
    time_sent = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    def __str__(self):
        return f"{time_sent}: From {by} to {to}"
