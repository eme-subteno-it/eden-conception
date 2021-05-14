# Generated by Django 3.2.2 on 2021-05-14 08:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('is_creator_user', models.BooleanField(default=False)),
                ('user_ids', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]