# Generated by Django 5.1.3 on 2025-01-15 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_note_is_encrypted_note_password_note_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
