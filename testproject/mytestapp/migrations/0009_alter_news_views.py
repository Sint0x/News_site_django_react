# Generated by Django 4.2.6 on 2023-11-03 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytestapp', '0008_remove_news_news_dislikes_remove_news_news_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='views',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]