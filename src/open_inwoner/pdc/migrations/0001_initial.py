# Generated by Django 3.2.7 on 2021-10-06 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("path", models.CharField(max_length=255, unique=True)),
                ("depth", models.PositiveIntegerField()),
                ("numchild", models.PositiveIntegerField(default=0)),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the category",
                        max_length=100,
                        verbose_name="name",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Slug of the category",
                        max_length=100,
                        unique=True,
                        verbose_name="slug",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="description"),
                ),
                (
                    "icon",
                    filer.fields.image.FilerImageField(
                        blank=True,
                        help_text="Icon of the category",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="category_icons",
                        to=settings.FILER_IMAGE_MODEL,
                    ),
                ),
                (
                    "image",
                    filer.fields.image.FilerImageField(
                        blank=True,
                        help_text="Image of the category",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="category_images",
                        to=settings.FILER_IMAGE_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "category",
                "verbose_name_plural": "categories",
            },
        ),
    ]
