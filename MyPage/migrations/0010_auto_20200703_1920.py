# Generated by Django 3.0.7 on 2020-07-03 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyPage', '0009_post_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='content',
            new_name='message',
        ),
    ]