# Generated by Django 4.2.2 on 2023-10-22 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfer_models', '0002_alter_datamodel_file_alter_sorteddatamodel_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sorteddatamodel',
            name='sorted_file',
            field=models.FileField(default=None, upload_to='sorted_files/%Y/%b/%d'),
        ),
    ]
