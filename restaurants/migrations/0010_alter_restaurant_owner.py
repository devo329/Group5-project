# Generated by Django 4.1.5 on 2023-02-09 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0009_reviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.owner'),
        ),
    ]
