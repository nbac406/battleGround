# Generated by Django 3.2.19 on 2023-07-04 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_alter_match_participant_matchid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match_participant',
            old_name='assist',
            new_name='assists',
        ),
    ]
