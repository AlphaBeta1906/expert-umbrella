# Generated by Django 4.1.10 on 2023-10-02 08:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_role_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="role",
            name="role_name",
            field=models.CharField(max_length=15),
        ),
    ]
