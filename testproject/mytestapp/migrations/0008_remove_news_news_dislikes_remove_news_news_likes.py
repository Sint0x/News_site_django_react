# Generated by Django 4.2.6 on 2023-11-02 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytestapp', '0007_alter_anonymousfeedback_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='news_dislikes',
        ),
        migrations.RemoveField(
            model_name='news',
            name='news_likes',
        ),
    ]