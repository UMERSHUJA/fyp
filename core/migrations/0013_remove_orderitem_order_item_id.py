# Generated by Django 3.1.3 on 2021-01-07 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20210107_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order_item_id',
        ),
    ]
