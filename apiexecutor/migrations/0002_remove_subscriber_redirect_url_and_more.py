# Generated by Django 5.0.2 on 2024-02-27 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiexecutor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriber',
            name='redirect_url',
        ),
        migrations.AddField(
            model_name='chargingsdks',
            name='redirect_url',
            field=models.URLField(default='http://127.0.0.1:8000/'),
            preserve_default=False,
        ),
    ]