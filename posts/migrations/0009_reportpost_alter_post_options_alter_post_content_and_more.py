# Generated by Django 4.1.10 on 2023-10-22 02:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0008_post_likes_alter_post_content_alter_post_tag"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReportPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.TextField(blank=True, default="")),
            ],
        ),
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ["-id"]},
        ),
        migrations.AlterField(
            model_name="post",
            name="content",
            field=models.TextField(
                help_text="This site are using markdown to writing content, You can find the guide at <a target='_blank' href='https://www.markdownguide.org/cheat-sheet/'>here</a> "
            ),
        ),
        migrations.DeleteModel(
            name="LikePost",
        ),
        migrations.AddField(
            model_name="reportpost",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="posts.post"
            ),
        ),
        migrations.AddField(
            model_name="reportpost",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
