# Generated by Django 3.1.6 on 2021-04-07 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_refund_requested_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('Mobile', 'Mobile'), ('Computer', 'Computer'), ('Television', 'Television'), ('Audio', 'Audio'), ('LargeAppliances', 'Large Appliances'), ('Camera', 'Camera')], max_length=15),
        ),
    ]
