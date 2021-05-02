from rest_framework import serializers

from .models import Artist, Album, Track


class ArtistSerializer(serializers.ModelSerializer):
  class Meta:
    model = Artist
    fields = ['id', 'name', 'age', 'albums', 'tracks', 'self_url']
    read_only_fields = ['id', 'albums', 'tracks', 'self_url']


class AlbumSerializer(serializers.ModelSerializer):
  #artist_id = serializers.CharField(source=id)

  class Meta:
    model = Album
    fields = ['id', 'artist_id', 'name', 'genre', 'artist', 'tracks', 'self_url']
    read_only_fields = ['id', 'artist_id', 'artist', 'tracks', 'self_url']

    depth =  1


class TrackSerializer(serializers.ModelSerializer):
  class Meta:
    model = Track
    fields = ['id', 'album_id', 'name', 'duration', 'times_played', 'artist', 'album', 'self_url']
    read_only_fields = ['id', 'album_id', 'times_played', 'artist', 'album', 'self_url']

    depth = 1