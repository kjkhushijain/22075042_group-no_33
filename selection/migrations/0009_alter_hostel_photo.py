# Generated by Django 4.2.6 on 2023-10-24 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selection', '0008_hostel_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostel',
            name='photo',
            field=models.ImageField(default='default.jpg', upload_to='documents/'),
        ),
    ]