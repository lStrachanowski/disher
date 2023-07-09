# Generated by Django 4.1 on 2023-07-02 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('dish_id', models.IntegerField()),
                ('owner', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User_Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_id', models.IntegerField()),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='disher.dish')),
            ],
        ),
        migrations.AddField(
            model_name='dish',
            name='products',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='disher.product'),
        ),
    ]
