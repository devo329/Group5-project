# Generated by Django 4.1.5 on 2023-03-05 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0029_deals_clipped_deals_clippers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]