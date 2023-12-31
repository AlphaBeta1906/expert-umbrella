# Generated by Django 4.1.10 on 2023-10-26 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0018_alter_post_is_hide_alter_tag_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="group",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="posts.grouppost",
            ),
        ),
    ]
