# Generated by Django 4.2.6 on 2023-11-05 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selection', '0022_resolvedcomplaint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='no_dues',
            field=models.BooleanField(default=False),
        ),
    ]