# Generated by Django 3.1.4 on 2020-12-07 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plagsample', '0002_plagsamp_file_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plagsamp',
            name='file_count',
            field=models.IntegerField(default=-1),
        ),
    ]