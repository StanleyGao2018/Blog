# Generated by Django 2.2.6 on 2019-10-24 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_articlepost_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='article/%Y%m%d/'),
        ),
    ]