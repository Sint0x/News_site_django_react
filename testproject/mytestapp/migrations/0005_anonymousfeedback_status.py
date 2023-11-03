# Generated by Django 4.2.6 on 2023-11-02 11:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytestapp', '0004_anonymousfeedback_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='anonymousfeedback',
            name='status',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
            preserve_default=False,
        ),
    ]
