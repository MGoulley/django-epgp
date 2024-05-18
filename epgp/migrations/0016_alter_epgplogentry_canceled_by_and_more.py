# Generated by Django 5.0.6 on 2024-05-18 21:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epgp', '0015_alter_player_isofficier'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='epgplogentry',
            name='canceled_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_canceled_by', to=settings.AUTH_USER_MODEL, verbose_name='Annulé par'),
        ),
        migrations.AlterField(
            model_name='epgplogentry',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='player_user_id', to=settings.AUTH_USER_MODEL, verbose_name='Attributeur'),
        ),
    ]