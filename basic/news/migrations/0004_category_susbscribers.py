# Generated by Django 4.2.2 on 2023-08-30 15:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0003_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='susbscribers',
            field=models.ManyToManyField(related_name='categories', to=settings.AUTH_USER_MODEL),
        ),
    ]
