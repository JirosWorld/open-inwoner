# Generated by Django 3.2.13 on 2022-07-04 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0045_alter_user_login_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='oidc_id',
            field=models.CharField(blank=True, default='', help_text='This field indicates if a user signed up with OpenId Connect or not.', max_length=250, verbose_name='OpenId Connect id'),
        ),
    ]
