# Generated by Django 3.2.17 on 2023-02-08 10:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_rename_readinggroup_reading_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='librarians',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]