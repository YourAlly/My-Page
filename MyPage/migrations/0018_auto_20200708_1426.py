# Generated by Django 3.0.7 on 2020-07-08 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyPage', '0017_remove_profile_hidden_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(),
        ),
    ]
