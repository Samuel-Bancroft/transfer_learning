# Generated by Django 4.2.2 on 2023-10-17 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfer_models', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datamodel',
            name='file',
            field=models.FileField(default='Default', upload_to='files/%Y/%b/%d'),
        ),
        migrations.AlterField(
            model_name='sorteddatamodel',
            name='file',
            field=models.FileField(default='Default', upload_to='files/%Y/%b/%d'),
        ),
    ]
