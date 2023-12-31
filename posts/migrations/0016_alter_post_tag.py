# Generated by Django 4.1.10 on 2023-10-24 15:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0015_alter_grouppost_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="tag",
            field=models.ManyToManyField(
                null=True, related_name="post_tags_set", to="posts.tag"
            ),
        ),
    ]
