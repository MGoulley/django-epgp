# Generated by Django 5.0.6 on 2024-05-12 13:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epgp', '0005_alter_loot_gameslot_alter_loot_ilvl_alter_loot_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='epgplogentry',
            name='canceled',
            field=models.BooleanField(default=False, verbose_name='Validité'),
        ),
        migrations.AlterField(
            model_name='epgplogentry',
            name='canceled_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_canceled_by', to='epgp.player', verbose_name='Effacé par'),
        ),
        migrations.AlterField(
            model_name='epgplogentry',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Créée le'),
        ),
        migrations.AlterField(
            model_name='epgplogentry',
            name='ep_delta',
            field=models.IntegerField(verbose_name='Modification en EP'),
        ),
        migrations.AlterField(
            model_name='epgplogentry',
            name='gp_delta',
            field=models.IntegerField(verbose_name='Modification en GP'),
        ),
        migrations.AlterField(
            model_name='epgplogentry',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='epgplogentry',
            name='reason',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Raison'),
        ),
        migrations.AlterField(
            model_name='epgplogentry',
            name='type',
            field=models.CharField(choices=[('DECAY', 'Decay'), ('DOCKEP', 'Dock EP'), ('DOCKGP', 'Dock GP'), ('LOOT', 'Loot'), ('PARTICIPATE', 'Participation'), ('STANDBY', 'Standby'), ('OTHER', 'Autre')], default='LOOT', max_length=20, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='epgplogentry',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modifié le'),
        ),
        migrations.CreateModel(
            name='Raid',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('played_at', models.DateTimeField(verbose_name='Date')),
                ('participants', models.ManyToManyField(to='epgp.character')),
            ],
        ),
    ]
