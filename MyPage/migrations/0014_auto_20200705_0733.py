# Generated by Django 3.0.7 on 2020-07-04 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyPage', '0013_auto_20200705_0645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.CharField(max_length=50),
        ),
    ]
