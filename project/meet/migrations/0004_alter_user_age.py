# Generated by Django 3.2.7 on 2021-10-07 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meet', '0003_auto_20211007_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.DateField(null=True),
        ),
    ]
