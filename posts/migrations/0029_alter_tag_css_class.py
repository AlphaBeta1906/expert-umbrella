# Generated by Django 4.1.10 on 2023-10-28 03:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0028_alter_tag_css_class"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="css_class",
            field=models.CharField(
                choices=[
                    ("t", "t"),
                    ("a", "a"),
                    ("g", "g"),
                    ("_", " "),
                    ("b", "b"),
                    ("l", "l"),
                    ("u", "u"),
                    ("e", "e"),
                    ("_", " "),
                    ("1", "1"),
                    ("0", "0"),
                    ("0", "0"),
                    ("\n", "\n"),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]
