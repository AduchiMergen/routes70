# Generated by Django 3.1.4 on 2020-12-14 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0004_auto_20201209_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stop',
            name='custom_id',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
