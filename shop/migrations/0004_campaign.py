# Generated by Django 2.2.6 on 2020-02-05 23:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20200206_0012'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('from_date', models.DateField(default=datetime.date.today)),
                ('to_date', models.DateField(default=datetime.date.today)),
                ('discount', models.FloatField(default=0.0)),
                ('country', models.CharField(blank=True, max_length=1000)),
            ],
        ),
    ]
