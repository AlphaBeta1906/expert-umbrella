# Generated by Django 4.1.10 on 2023-10-30 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0039_postcontent_remove_post_content_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="content",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="posts.postcontent",
            ),
        ),
    ]
