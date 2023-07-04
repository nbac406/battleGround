# Generated by Django 3.2.19 on 2023-07-04 03:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_auto_20230703_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match_summary',
            name='matchId',
            field=models.ForeignKey(max_length=200, on_delete=django.db.models.deletion.CASCADE, to='services.players'),
        ),
        migrations.AlterField(
            model_name='players',
            name='matchId',
            field=models.CharField(max_length=200),
        ),
    ]