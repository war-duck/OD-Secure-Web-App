# Generated by Django 5.1.3 on 2025-01-13 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_note_title_note_created_at_note_is_public_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='is_encrypted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='note',
            name='password',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='note',
            name='title',
            field=models.CharField(default='Untitled', max_length=100),
        ),
    ]
