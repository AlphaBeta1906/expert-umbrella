# Generated by Django 4.1.10 on 2023-10-31 01:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0044_alter_post_summary"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="summary",
            field=models.TextField(
                default="No summary",
                max_length=250,
                null=True,
                verbose_name="Post summary",
            ),
        ),
    ]
