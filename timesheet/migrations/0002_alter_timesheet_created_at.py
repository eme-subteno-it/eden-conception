# Generated by Django 3.2.2 on 2021-06-17 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheet',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
