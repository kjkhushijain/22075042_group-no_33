# Generated by Django 4.2.6 on 2023-10-23 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selection', '0005_document_student_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostel',
            name='friday_menu',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='hostel',
            name='monday_menu',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='hostel',
            name='saturday_menu',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='hostel',
            name='sunday_menu',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='hostel',
            name='thursday_menu',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='hostel',
            name='tuesday_menu',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='hostel',
            name='wednesday_menu',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]