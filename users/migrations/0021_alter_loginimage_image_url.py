# Generated by Django 4.2.7 on 2023-11-15 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_loginimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginimage',
            name='image_url',
            field=models.URLField(help_text='twitter url to an image'),
        ),
    ]