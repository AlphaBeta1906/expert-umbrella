# Generated by Django 4.1.10 on 2023-11-01 00:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0046_alter_post_is_complete_alter_post_is_draft"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="grouppost",
            options={"ordering": ["-id"]},
        ),
        migrations.AddField(
            model_name="post",
            name="date_publish",
            field=models.DateTimeField(null=True),
        ),
    ]
