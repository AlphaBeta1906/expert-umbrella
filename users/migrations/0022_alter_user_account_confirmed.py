# Generated by Django 4.2.7 on 2023-11-15 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_alter_loginimage_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_confirmed',
            field=models.BooleanField(default=False, help_text='confirm user account'),
        ),
    ]
