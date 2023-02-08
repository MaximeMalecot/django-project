# Generated by Django 3.2.17 on 2023-02-08 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_alter_library_librarians'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='library',
            name='librarians',
        ),
        migrations.AddField(
            model_name='user',
            name='library',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='library.library'),
        ),
    ]