# Generated by Django 3.2 on 2022-11-11 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_bannerslider_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bannerslider',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True),
        ),
    ]
