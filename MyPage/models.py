from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="written_posts")
    time_posted = models.DateTimeField(default=timezone.now)
    
    title = models.CharField(max_length=64, default='No Title')
    content = models.TextField()

    def __str__(self):
        return f"{self.author}: {self.time_posted}"


class Comment(models.Model):
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="written_comments")
    on_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments")
    time_commented = models.DateTimeField(default=timezone.now)
    
    comment = models.TextField()

    def __str__(self):
        return f"{self.commenter}: {self.time_commented} - {self.on_post} "


class Message(models.Model):
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE,
                           related_name='sent_messages')
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE,
                           related_name='recieved_messages')
    time_sent = models.DateTimeField(default=timezone.now)

    message = models.TextField()

    def __str__(self):
        return f"{self.time_sent}: From {self.sent_by} to {self.sent_to}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='images')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    hidden_posts = models.ManyToManyField(Post, blank=True)

    def __str__(self):
        return f'Profile: {self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
