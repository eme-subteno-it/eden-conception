# Generated by Django 3.2.2 on 2021-07-16 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='is_done',
            field=models.BooleanField(default=0),
        ),
    ]
