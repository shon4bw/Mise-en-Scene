# Generated by Django 3.2.9 on 2021-11-21 05:45

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_remove_movie_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='video',
            field=embed_video.fields.EmbedVideoField(null=True),
        ),
    ]