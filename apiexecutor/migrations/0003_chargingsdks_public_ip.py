# Generated by Django 5.0.2 on 2024-02-27 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiexecutor', '0002_remove_subscriber_redirect_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chargingsdks',
            name='public_ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
