# Generated by Django 4.1.10 on 2023-10-15 09:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_role_role_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="ban",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="profile",
            field=models.TextField(
                help_text="Tell about yourself(max: 250 characthers)",
                max_length=250,
                null=True,
                verbose_name="User profile",
            ),
        ),
    ]
