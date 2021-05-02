from django.urls import path, include
from rest_framework import routers

from .views import ArtistViewset, AlbumViewset, TrackViewset


# Ver todos los artistas
artists_list = ArtistViewset.as_view({
  'get': 'list',
  'post': 'create'
  })

# ver detalles de un artista
artists_detail = ArtistViewset.as_view({
  'get': 'retrieve',
  'delete': 'destroy'
  })

artist_play = ArtistViewset.as_view({
  'put': 'update'
})

# ver todos los albums
albums_list = AlbumViewset.as_view({
  'get': 'list',
  })

# ver detalles de un album
albums_detail = AlbumViewset.as_view({
  'get': 'retrieve',
  'delete': 'destroy'
  })

albums_artist = AlbumViewset.as_view({
  'get': 'get_artist_albums',
  'post': 'create'
  })

album_play = AlbumViewset.as_view({
  'put': 'update'
})  

# ver todos las canciones
tracks_list = TrackViewset.as_view({
  'get': 'list',
  })

# ver detalles de un album
tracks_detail = TrackViewset.as_view({
  'get': 'retrieve',
  'delete': 'destroy',
  })

tracks_album = TrackViewset.as_view({
  'get': 'get_tracks_album',
  'post': 'create'
  })

tracks_artist = TrackViewset.as_view({
  'get': 'get_tracks_artist'
})

tracks_play = TrackViewset.as_view({
  'put': 'update'
})


urlpatterns = [
  path('artists/', artists_list, name='artist'),
  path('artists/<str:id>/', artists_detail, name='artist_detail'),
  path('artists/<str:id>/tracks', tracks_artist, name='show_tracks'),
  path('artists/<str:id>/albums', albums_artist, name='create_album'), 
  path('artists/<str:id>/albums/play', artist_play, name='play_artist'), 

  path('albums/', albums_list, name='album'), 
  path('albums/<str:id>/', albums_detail, name='albums_detail'),
  path('albums/<str:id>/tracks', tracks_album, name='create_track'),
  path('albums/<str:id>/tracks/play', album_play , name='play_album'),

  path('tracks/', tracks_list, name='tracks'),
  path('tracks/<str:id>', tracks_detail, name='tracks_detail'),
  path('tracks/<str:id>/play', tracks_play, name='play_track'),

]

