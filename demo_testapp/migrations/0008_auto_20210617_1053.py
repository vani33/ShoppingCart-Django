# Generated by Django 3.2.4 on 2021-06-17 05:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo_testapp', '0007_auto_20210617_1047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
