# Generated by Django 5.0.2 on 2024-03-11 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0003_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='experience',
            field=models.CharField(max_length=20),
        ),
    ]
