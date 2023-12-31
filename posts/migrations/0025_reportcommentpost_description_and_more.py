# Generated by Django 4.1.10 on 2023-10-28 00:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0024_post_date_updated_alter_post_date_created"),
    ]

    operations = [
        migrations.AddField(
            model_name="reportcommentpost",
            name="description",
            field=models.TextField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name="commentpost",
            name="content",
            field=models.TextField(
                max_length=250, verbose_name="Your comment"
            ),
        ),
        migrations.AlterField(
            model_name="reportcommentpost",
            name="reason",
            field=models.CharField(
                choices=[
                    ("Unappropriate content", "Unappropriate content"),
                    ("Another report", "Another report"),
                ],
                max_length=50,
            ),
        ),
    ]
