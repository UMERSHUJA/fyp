# Generated by Django 3.1.3 on 2021-01-08 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20210108_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='stock',
            field=models.IntegerField(default=100),
        ),
    ]
