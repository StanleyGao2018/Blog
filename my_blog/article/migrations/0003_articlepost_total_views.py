# Generated by Django 2.2.6 on 2019-10-21 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20191017_0542'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='total_views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
