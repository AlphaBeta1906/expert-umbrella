# Generated by Django 4.2.7 on 2023-11-12 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_userban_ban_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='userban',
            name='ban_category',
            field=models.CharField(default=None, max_length=150),
            preserve_default=False,
        ),
    ]
