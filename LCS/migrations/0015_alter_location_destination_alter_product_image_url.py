# Generated by Django 4.0.6 on 2022-08-15 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LCS', '0014_product_image_url_alter_location_destination'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='destination',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_url',
            field=models.CharField(default='', max_length=500),
        ),
    ]
