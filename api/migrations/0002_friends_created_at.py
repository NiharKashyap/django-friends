# Generated by Django 5.0.6 on 2024-06-15 18:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friends',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]