# Generated by Django 3.1.4 on 2020-12-17 06:16
from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0006_auto_20201214_0943'),
    ]

    operations = [
        TrigramExtension()
    ]
