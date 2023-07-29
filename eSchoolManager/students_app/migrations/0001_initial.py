# Generated by Django 4.2.1 on 2023-07-25 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import eSchoolManager.students_app.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classes_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], default=None, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, null=True, validators=[eSchoolManager.students_app.validators.CheckIfValidPhone(), eSchoolManager.students_app.validators.CheckIfValidLength()])),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('school_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='classes_app.classesmodel')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
