# Generated by Django 5.0.2 on 2024-02-27 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiexecutor', '0003_chargingsdks_public_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='masked_msisdn',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
