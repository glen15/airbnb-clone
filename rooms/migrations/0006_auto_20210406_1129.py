# Generated by Django 2.2.5 on 2021-04-06 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_auto_20210406_1041'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='discription',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='pircie',
            new_name='price',
        ),
    ]