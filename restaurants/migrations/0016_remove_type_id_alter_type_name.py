# Generated by Django 4.1.5 on 2023-02-12 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0015_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='type',
            name='id',
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=60, primary_key=True, serialize=False),
        ),
    ]
