# Generated by Django 3.2.3 on 2021-05-19 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20210515_0049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ccnjobcard',
            name='model_no',
        ),
        migrations.RemoveField(
            model_name='ccnjobcard',
            name='sr_no',
        ),
        migrations.CreateModel(
            name='PrinterJobCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sr_no', models.CharField(max_length=30, null=True)),
                ('model_no', models.CharField(max_length=200, null=True)),
                ('ccn_job_card', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.ccnjobcard')),
            ],
        ),
    ]
