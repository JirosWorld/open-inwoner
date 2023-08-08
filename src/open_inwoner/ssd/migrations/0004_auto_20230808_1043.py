# Generated by Django 3.2.15 on 2023-08-08 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ssd", "0003_auto_20230802_1635"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ssdconfig",
            name="jaaropgave_display_text",
            field=models.TextField(
                blank=True,
                help_text="The text displayed as overview of the 'Jaaropgave' tab",
                verbose_name="Display text",
            ),
        ),
        migrations.AlterField(
            model_name="ssdconfig",
            name="jaaropgave_endpoint",
            field=models.CharField(
                default="JaarOpgaveClient-v0400",
                help_text="Endpoint for the jaaropgave request",
                max_length=256,
                verbose_name="Jaaropgave endpoint",
            ),
        ),
        migrations.AlterField(
            model_name="ssdconfig",
            name="maandspecificatie_display_text",
            field=models.TextField(
                blank=True,
                help_text="The text displayed as overview of the 'Maandspecificatie' tab",
                verbose_name="Display text",
            ),
        ),
        migrations.AlterField(
            model_name="ssdconfig",
            name="maandspecificatie_endpoint",
            field=models.CharField(
                default="UitkeringsSpecificatieClient-v0600",
                help_text="Endpoint for the maandspecificatie request",
                max_length=256,
                verbose_name="Maandspecificatie endpoint",
            ),
        ),
        migrations.AlterField(
            model_name="ssdconfig",
            name="mijn_uitkeringen_text",
            field=models.TextField(
                blank=True,
                help_text="The text displayed as overview of the 'Mijn Uikeringen' section.",
                verbose_name="Overview text",
            ),
        ),
    ]
