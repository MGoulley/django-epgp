# Generated by Django 5.0.6 on 2024-05-18 17:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epgp', '0013_remove_epgplogentry_source_player_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='epgplogentry',
            name='target_player_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_target_player_id', to='epgp.player', verbose_name='Joueur'),
        ),
    ]
