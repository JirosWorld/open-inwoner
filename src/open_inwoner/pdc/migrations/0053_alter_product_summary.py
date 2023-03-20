# Generated by Django 3.2.15 on 2023-03-02 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pdc", "0052_auto_20230221_1518"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="summary",
            field=models.TextField(
                default="",
                help_text="Short description of the product, limited to 300 characters.",
                max_length=300,
                verbose_name="Summary",
            ),
        ),
    ]