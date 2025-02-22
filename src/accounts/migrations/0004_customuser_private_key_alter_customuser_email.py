# Generated by Django 5.1.3 on 2025-01-15 14:11

import accounts.models
import encrypted_model_fields.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='private_key',
            field=encrypted_model_fields.fields.EncryptedCharField(default=accounts.models.initialize_private_key),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, default='a@a.com', max_length=254),
        ),
    ]
