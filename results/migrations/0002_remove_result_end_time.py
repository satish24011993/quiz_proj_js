# Generated by Django 3.0.5 on 2021-03-26 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='end_time',
        ),
    ]
