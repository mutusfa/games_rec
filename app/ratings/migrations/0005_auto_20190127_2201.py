# Generated by Django 2.1.5 on 2019-01-27 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0004_auto_20190127_2154'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('player', 'game')},
        ),
    ]