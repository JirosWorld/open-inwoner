# Generated by Django 3.2.15 on 2023-06-21 09:43

from django.db import migrations


def populate_order_of_subjects(apps, schema_editor):
    Subject = apps.get_model("openklant", "ContactFormSubject")
    for subject in Subject.objects.all():
        subject.order = subject.pk
        subject.save()


class Migration(migrations.Migration):
    dependencies = [
        ("openklant", "0004_auto_20230621_1142"),
    ]

    operations = [
        migrations.RunPython(
            populate_order_of_subjects, reverse_code=migrations.RunPython.noop
        ),
    ]