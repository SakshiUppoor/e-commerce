# Generated by Django 2.2.6 on 2020-02-06 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20200206_0530'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='user',
            name='facebook',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='user',
            name='twitter',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]