# Generated by Django 3.2.3 on 2021-05-19 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_ccnjobcard_model_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='printerjobcard',
            name='type_of_problem',
            field=models.CharField(max_length=200, null=True),
        ),
    ]