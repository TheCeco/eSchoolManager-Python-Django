# Generated by Django 4.2.1 on 2023-07-28 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teacherclass',
            options={'ordering': ['school_class']},
        ),
    ]
