# Generated by Django 4.2.1 on 2023-08-06 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='principalprofile',
            name='image_url',
            field=models.URLField(blank=True, default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRb7b5Uk6-fslFsGiTi_zqcNqdn9QqIC8AMxw&usqp=CAU', null=True),
        ),
    ]
