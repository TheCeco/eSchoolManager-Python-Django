# Generated by Django 4.2.1 on 2023-08-09 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common_app', '0002_alter_subjectsmodel_subject_name'),
        ('classes_app', '0002_alter_teacherclass_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherclass',
            name='subject',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='common_app.subjectsmodel'),
            preserve_default=False,
        ),
    ]
