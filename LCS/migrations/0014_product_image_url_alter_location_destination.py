# Generated by Django 4.0.6 on 2022-08-15 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LCS', '0013_alter_order_item_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='location',
            name='destination',
            field=models.CharField(default='', max_length=40),
        ),
    ]
