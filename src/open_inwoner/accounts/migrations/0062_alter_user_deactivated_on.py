# Generated by Django 3.2.15 on 2023-06-23 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0061_auto_20230612_1428"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="deactivated_on",
            field=models.DateField(
                blank=True,
                help_text="This is the date the user decided to deactivate their account. This field is deprecated since user profiles are now immediately deleted.",
                null=True,
                verbose_name="Deactivated on",
            ),
        ),
    ]