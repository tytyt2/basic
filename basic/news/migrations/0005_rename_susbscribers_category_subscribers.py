# Generated by Django 4.2.2 on 2023-09-20 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_category_susbscribers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='susbscribers',
            new_name='subscribers',
        ),
    ]