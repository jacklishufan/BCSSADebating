# Generated by Django 2.2.4 on 2019-10-30 23:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qipashuo', '0008_finalspeaker_finalvoter_grandfinal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='finalspeaker',
            old_name='name',
            new_name='speaker_name',
        ),
    ]
