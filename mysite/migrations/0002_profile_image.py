# Generated by Django 3.2.4 on 2021-07-04 19:35

from django.db import migrations, models
import mysite.models.profile_models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to=mysite.models.profile_models.upload_image_to),
        ),
    ]
