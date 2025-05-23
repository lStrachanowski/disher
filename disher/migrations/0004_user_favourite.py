# Generated by Django 4.1 on 2024-08-24 20:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('disher', '0003_product_amount_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Favourite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='disher.dish')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
