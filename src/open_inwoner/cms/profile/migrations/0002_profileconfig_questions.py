# Generated by Django 3.2.15 on 2023-05-23 07:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profile", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profileconfig",
            name="questions",
            field=models.BooleanField(
                default=True,
                help_text="Designates whether 'questions' section is rendered or not.",
                verbose_name="Mijn vragen",
            ),
        ),
    ]