# Generated by Django 2.2.4 on 2019-10-07 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qipashuo', '0002_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ballot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Scoring',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='index',
        ),
        migrations.AddField(
            model_name='scoring',
            name='scored_speaker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qipashuo.Speaker'),
        ),
        migrations.AddField(
            model_name='round',
            name='speakers',
            field=models.ManyToManyField(to='qipashuo.Speaker'),
        ),
        migrations.AddField(
            model_name='ballot',
            name='scorings',
            field=models.ManyToManyField(to='qipashuo.Scoring'),
        ),
        migrations.AddField(
            model_name='ballot',
            name='voter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qipashuo.User'),
        ),
    ]
