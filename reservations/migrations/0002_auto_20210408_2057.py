# Generated by Django 2.2.5 on 2021-04-08 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('comfirmed', 'Confirmed'), ('canceld', 'Canceled')], max_length=12),
        ),
    ]