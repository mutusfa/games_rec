# Generated by Django 2.1.5 on 2019-01-21 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0002_auto_20181227_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='bgg_id',
            field=models.IntegerField(blank=True, default=None, null=True, unique=True),
        ),
    ]
