# Generated by Django 2.2.4 on 2019-08-13 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20190812_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='short_description',
            field=models.TextField(default='Description Available at Item Page', verbose_name='Product Short Description'),
        ),
    ]
