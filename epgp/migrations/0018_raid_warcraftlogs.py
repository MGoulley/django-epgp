# Generated by Django 5.0.6 on 2024-05-19 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epgp', '0017_alter_character_ilvl_alter_character_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='raid',
            name='warcraftLogs',
            field=models.URLField(blank=True, null=True, verbose_name='URL Warcraft Logs'),
        ),
    ]
