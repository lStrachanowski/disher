# Generated by Django 4.1 on 2024-10-08 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disher', '0004_user_favourite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_favourite',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
