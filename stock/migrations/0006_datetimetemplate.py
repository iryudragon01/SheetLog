# Generated by Django 2.2.6 on 2019-11-02 04:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_auto_20191101_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateTimeTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime(2019, 11, 2, 11, 31, 51, 949201))),
                ('time', models.TimeField(default=datetime.datetime(2019, 11, 2, 11, 31, 51, 949201))),
            ],
        ),
    ]
