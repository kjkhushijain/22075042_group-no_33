# Generated by Django 4.2.6 on 2023-10-25 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selection', '0010_complaint'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='complaint',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.RenameField(
            model_name='complaint',
            old_name='created_at',
            new_name='created',
        ),
        migrations.AddField(
            model_name='complaint',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
