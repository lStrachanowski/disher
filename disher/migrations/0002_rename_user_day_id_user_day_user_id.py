# Generated by Django 4.1 on 2023-11-04 00:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('disher', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_day',
            old_name='user_day_id',
            new_name='user_id',
        ),
    ]