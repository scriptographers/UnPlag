# Generated by Django 3.1.4 on 2020-12-07 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plagsample', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plagsamp',
            name='file_count',
            field=models.IntegerField(default=0),
        ),
    ]
