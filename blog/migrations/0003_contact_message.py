# Generated by Django 5.0.2 on 2024-02-23 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_contact_subject_contact_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
