# Generated by Django 3.2.2 on 2021-05-20 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_rename_user_id_project_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=120, unique=True),
        ),
    ]