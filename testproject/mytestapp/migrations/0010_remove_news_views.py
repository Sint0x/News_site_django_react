# Generated by Django 4.2.6 on 2023-11-03 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytestapp', '0009_alter_news_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='views',
        ),
    ]