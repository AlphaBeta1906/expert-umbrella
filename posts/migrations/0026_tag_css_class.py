# Generated by Django 4.1.10 on 2023-10-28 00:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0025_reportcommentpost_description_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tag",
            name="css_class",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
