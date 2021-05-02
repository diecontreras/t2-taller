# Generated by Django 3.2 on 2021-05-02 01:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.CharField(max_length=22, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('genre', models.CharField(max_length=255)),
                ('artist', models.CharField(max_length=255)),
                ('tracks', models.CharField(max_length=255)),
                ('self_url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.CharField(max_length=22, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('albums', models.CharField(max_length=255)),
                ('tracks', models.CharField(max_length=255)),
                ('self_url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.CharField(max_length=22, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('duration', models.FloatField()),
                ('times_played', models.IntegerField()),
                ('artist', models.CharField(max_length=255)),
                ('album', models.CharField(max_length=255)),
                ('self_url', models.CharField(max_length=255)),
                ('album_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spotifly.album')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='artist_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spotifly.artist'),
        ),
    ]
