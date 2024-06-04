# Generated by Django 5.0.6 on 2024-06-04 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epgp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raid',
            name='instance',
            field=models.CharField(choices=[('ICC', 'Icecrown Citadel'), ('BARADIN', 'Baradin Hold'), ('BASTION', 'Bastion of Twilight'), ('THRONE', 'Throne of the Four Winds'), ('BLACKWING', 'Blackwing Descent'), ('FIRELAND', 'Firelands'), ('DRAGON', 'Dragon Soul'), ('AUTRE', 'Autre')], default='BARADIN', max_length=20, verbose_name='Instance'),
        ),
    ]