# Generated by Django 3.2.1 on 2021-05-14 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20210515_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='current_address',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='permanent_address',
            field=models.TextField(blank=True, max_length=100),
        ),
    ]
