# Generated by Django 2.0.1 on 2018-03-23 04:26

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='skills',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None), default=[['number theory', '0'], ['inequalities', '0'], ['polynoms', '0'], ['functions', '0']], size=None),
        ),
    ]
