# Generated by Django 4.1.10 on 2023-10-31 00:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0043_delete_postcontent_alter_post_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="summary",
            field=models.TextField(
                blank=True,
                default="No summary",
                null=True,
                verbose_name="Post summary",
            ),
        ),
    ]
