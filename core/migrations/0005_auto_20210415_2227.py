# Generated by Django 3.0 on 2021-04-15 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210415_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selecteddata',
            name='user',
            field=models.CharField(max_length=255),
        ),
    ]