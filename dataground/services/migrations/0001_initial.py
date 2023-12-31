# Generated by Django 3.2.19 on 2023-08-02 01:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='players',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.CharField(max_length=100)),
                ('player_name', models.CharField(max_length=100)),
                ('shard_id', models.CharField(max_length=100)),
                ('match_id', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField()),
            ],
            options={
                'unique_together': {('account_id', 'match_id')},
            },
        ),
        migrations.CreateModel(
            name='weapons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weapon_name', models.CharField(max_length=100, unique=True)),
                ('weapon_type', models.CharField(max_length=20)),
                ('weapon_tier', models.IntegerField()),
                ('first_easy_weapon', models.CharField(max_length=30)),
                ('first_easy_percent', models.FloatField()),
                ('second_easy_weapon', models.CharField(max_length=30)),
                ('second_easy_percent', models.FloatField()),
                ('third_easy_weapon', models.CharField(max_length=30)),
                ('third_easy_percent', models.FloatField()),
                ('first_hard_weapon', models.CharField(max_length=30)),
                ('first_hard_percent', models.FloatField()),
                ('second_hard_weapon', models.CharField(max_length=30)),
                ('second_hard_percent', models.FloatField()),
                ('third_hard_weapon', models.CharField(max_length=30)),
                ('third_hard_percent', models.FloatField()),
                ('graph_image_url', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='weapon_parts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weapon_name', models.CharField(max_length=100)),
                ('parts_name', models.CharField(max_length=100)),
                ('parts_type', models.CharField(max_length=50)),
                ('utilization_rate', models.FloatField()),
                ('weapons_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.weapons')),
            ],
        ),
        migrations.CreateModel(
            name='weapon_masterys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.CharField(max_length=100, unique=True)),
                ('first_weapon_name', models.CharField(max_length=100)),
                ('first_weapon_XPtotal', models.IntegerField()),
                ('second_weapon_name', models.CharField(max_length=100)),
                ('second_weapon_XPtotal', models.IntegerField()),
                ('third_weapon_name', models.CharField(max_length=100)),
                ('third_weapon_XPtotal', models.IntegerField()),
                ('weapon_cluster', models.CharField(max_length=20)),
                ('players_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.players')),
            ],
        ),
        migrations.CreateModel(
            name='match_summarys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_id', models.CharField(max_length=200, unique=True)),
                ('game_mode', models.CharField(max_length=20)),
                ('map_name', models.CharField(max_length=30)),
                ('duration', models.IntegerField()),
                ('match_type', models.CharField(max_length=20)),
                ('asset_url', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField()),
                ('players_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.players')),
            ],
        ),
        migrations.CreateModel(
            name='maps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('map_name', models.CharField(max_length=20)),
                ('start_point', models.IntegerField()),
                ('end_point', models.IntegerField()),
                ('image_url', models.CharField(max_length=1000)),
            ],
            options={
                'unique_together': {('map_name', 'start_point', 'end_point')},
            },
        ),
        migrations.CreateModel(
            name='position_logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_id', models.CharField(max_length=200)),
                ('player_name', models.CharField(max_length=100)),
                ('account_id', models.CharField(max_length=200)),
                ('location_x', models.FloatField()),
                ('location_y', models.FloatField()),
                ('event_time', models.IntegerField()),
                ('players_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.players')),
            ],
            options={
                'unique_together': {('account_id', 'match_id', 'event_time')},
            },
        ),
        migrations.CreateModel(
            name='match_participants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_id', models.CharField(max_length=200)),
                ('player_name', models.CharField(max_length=100)),
                ('account_id', models.CharField(max_length=200)),
                ('roster_id', models.CharField(max_length=200)),
                ('team_ranking', models.IntegerField()),
                ('dbnos', models.IntegerField()),
                ('assists', models.IntegerField()),
                ('damage_dealt', models.FloatField()),
                ('headshot_kills', models.IntegerField()),
                ('kills', models.IntegerField()),
                ('longest_kill', models.IntegerField()),
                ('team_kills', models.IntegerField()),
                ('ride_distance', models.FloatField()),
                ('swim_distance', models.FloatField()),
                ('walk_distance', models.FloatField()),
                ('players_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.players')),
            ],
            options={
                'unique_together': {('account_id', 'match_id')},
            },
        ),
        migrations.CreateModel(
            name='kill_logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_id', models.CharField(max_length=200)),
                ('victim_name', models.CharField(max_length=100)),
                ('killer_name', models.CharField(max_length=100)),
                ('victim_account_id', models.CharField(max_length=200)),
                ('killer_account_id', models.CharField(max_length=200)),
                ('victim_x', models.FloatField()),
                ('victim_y', models.FloatField()),
                ('killer_x', models.FloatField()),
                ('killer_y', models.FloatField()),
                ('event_time', models.IntegerField()),
                ('players_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.players')),
            ],
            options={
                'unique_together': {('match_id', 'victim_account_id', 'killer_account_id')},
            },
        ),
    ]
