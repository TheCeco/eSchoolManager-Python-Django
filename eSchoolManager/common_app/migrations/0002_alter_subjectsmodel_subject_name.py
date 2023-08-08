# Generated by Django 4.2.1 on 2023-08-08 21:56

from django.db import migrations, models
import eSchoolManager.common_app.validators


class Migration(migrations.Migration):

    dependencies = [
        ('common_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjectsmodel',
            name='subject_name',
            field=models.CharField(max_length=50, unique=True, validators=[eSchoolManager.common_app.validators.NoNumInName()]),
        ),
    ]
