# Generated by Django 5.2 on 2025-04-18 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="index",
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
