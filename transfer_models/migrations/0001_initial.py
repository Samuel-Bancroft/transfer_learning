# Generated by Django 4.2.2 on 2023-06-21 08:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('comment', models.EmailField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='CreateModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('model_name', models.CharField(default='Default', max_length=100)),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('file_type', models.CharField(default=None, max_length=10)),
                ('file_data_type', models.CharField(default=None, max_length=20)),
                ('columns', models.CharField(default='default', max_length=1000)),
                ('created_by', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Created Models',
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='FileToJSON',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='SortedModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('model_name', models.CharField(default='Default', max_length=100)),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('file_type', models.CharField(default=None, max_length=10)),
                ('file_data_type', models.CharField(default=None, max_length=20)),
                ('columns', models.CharField(default=None, max_length=1000)),
                ('converted_columns', models.CharField(default=None, max_length=1000)),
                ('removed_columns', models.CharField(default=None, max_length=1000)),
                ('created_by', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('from_file', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='transfer_models.createmodel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
