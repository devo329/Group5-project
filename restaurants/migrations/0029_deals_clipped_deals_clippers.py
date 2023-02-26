# Generated by Django 4.1.5 on 2023-02-25 21:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurants', '0028_alter_owner_first_name_alter_owner_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deals',
            name='clipped',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='deals',
            name='clippers',
            field=models.ManyToManyField(blank=True, related_name='clippers', to=settings.AUTH_USER_MODEL),
        ),
    ]