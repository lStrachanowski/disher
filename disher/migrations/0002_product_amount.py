# Generated by Django 4.1 on 2023-09-06 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_Amount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('dish', models.ManyToManyField(to='disher.dish')),
                ('product_name', models.ManyToManyField(to='disher.product')),
            ],
        ),
    ]