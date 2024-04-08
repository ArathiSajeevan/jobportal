# Generated by Django 5.0.2 on 2024-03-13 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_alter_job_experience'),
    ]

    operations = [
        migrations.CreateModel(
            name='jobapply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('designation', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('qualification', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('experience', models.CharField(max_length=20)),
                ('image', models.FileField(upload_to='job/static')),
            ],
        ),
    ]
