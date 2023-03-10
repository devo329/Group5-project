# Generated by Django 4.1.5 on 2023-02-25 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0027_deals_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='first_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='owner',
            name='last_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='banner_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='doordashlink',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='image_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='uberlink',
            field=models.CharField(default='', max_length=255),
        ),
    ]
