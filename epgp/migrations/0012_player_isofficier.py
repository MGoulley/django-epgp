# Generated by Django 5.0.6 on 2024-05-17 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epgp', '0011_alter_raid_instance_alter_raid_played_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='isOfficier',
            field=models.BooleanField(default=False),
        ),
    ]