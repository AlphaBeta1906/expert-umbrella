# Generated by Django 4.1.10 on 2023-11-01 01:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0047_alter_grouppost_options_post_date_publish"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="date_publish",
            new_name="date_published",
        ),
    ]
