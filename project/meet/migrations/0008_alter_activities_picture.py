# Generated by Django 3.2.7 on 2021-10-09 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meet', '0007_activities_hobby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activities',
            name='picture',
            field=models.ImageField(upload_to='img'),
        ),
    ]
