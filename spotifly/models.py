from django.db import models


# Clase Artist
class Artist(models.Model):
  id = models.CharField(max_length=22, primary_key=True)
  name = models.CharField(max_length=255)
  age = models.IntegerField()
  albums = models.CharField(max_length=255)
  tracks = models.CharField(max_length=255)
  self_url = models.CharField(max_length=255)

  def __str__(self):
    return self.name


# Clase Album
class Album(models.Model):
  id = models.CharField(max_length=22, primary_key=True)
  artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE, null=False)
  name = models.CharField(max_length=255)
  genre = models.CharField(max_length=255)
  artist = models.CharField(max_length=255)
  tracks = models.CharField(max_length=255)
  self_url = models.CharField(max_length=255)

  def __str__(self):
    return self.name


# Clase Track
class Track(models.Model):
  id = models.CharField(max_length=22, primary_key=True)
  album_id = models.ForeignKey(Album, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  duration = models.FloatField()
  times_played = models.IntegerField()
  artist = models.CharField(max_length=255)
  album = models.CharField(max_length=255)
  self_url = models.CharField(max_length=255)

  def __str__(self):
    return self.name
