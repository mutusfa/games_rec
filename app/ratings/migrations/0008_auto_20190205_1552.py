# Generated by Django 2.1.5 on 2019-02-05 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0007_game_standalone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='standalone',
            field=models.BooleanField(default=True),
        ),
    ]
