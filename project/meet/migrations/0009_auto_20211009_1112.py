# Generated by Django 3.2.7 on 2021-10-09 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meet', '0008_alter_activities_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='countries',
            old_name='user_hobby',
            new_name='user_country',
        ),
        migrations.AddField(
            model_name='events',
            name='event_location',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='eventLocation', to='meet.countries'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='activities',
            name='picture',
            field=models.ImageField(upload_to='img/%y'),
        ),
    ]
