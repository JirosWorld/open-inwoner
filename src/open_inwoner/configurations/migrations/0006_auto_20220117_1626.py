# Generated by Django 3.2.7 on 2022-01-17 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("configurations", "0005_auto_20220110_1042"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteconfiguration",
            name="account_help_text",
            field=models.TextField(
                blank=True,
                default="Op dit scherm ziet u uw persoonlijke profielgegevens en gerelateerde gegevens.",
                help_text="The help text for the profile page.",
                verbose_name="Account help",
            ),
        ),
        migrations.AddField(
            model_name="siteconfiguration",
            name="home_help_text",
            field=models.TextField(
                blank=True,
                default="Welkom! Op dit scherm vindt u een overzicht van de verschillende thema's en producten & diensten.",
                help_text="The help text for the home page.",
                verbose_name="Home help",
            ),
        ),
        migrations.AddField(
            model_name="siteconfiguration",
            name="product_help_text",
            field=models.TextField(
                blank=True,
                default="Op dit scherm kunt u de details vinden over het gekozen product of dienst. Afhankelijk van het product kunt u deze direct aanvragen of meer informatie opvragen.",
                help_text="The help text for the product page.",
                verbose_name="Product help",
            ),
        ),
        migrations.AddField(
            model_name="siteconfiguration",
            name="search_help_text",
            field=models.TextField(
                blank=True,
                default="Op dit scherm kunt u zoeken naar de producten en diensten.",
                help_text="The help text for the search page.",
                verbose_name="Search help",
            ),
        ),
        migrations.AddField(
            model_name="siteconfiguration",
            name="theme_help_text",
            field=models.TextField(
                blank=True,
                default="Op dit scherm vindt u de verschillende thema's waarvoor wij producten en diensten aanbieden.",
                help_text="The help text for the theme page.",
                verbose_name="Theme help",
            ),
        ),
    ]
