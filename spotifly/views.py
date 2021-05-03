from rest_framework.response import Response
from rest_framework import viewsets, status
from base64 import b64encode

from .models import Artist, Album, Track
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer


class ArtistViewset(viewsets.ModelViewSet):
  serializer_class = ArtistSerializer
  queryset = ''

  def list(self, request):
    """ Usado para obtener todos los artistas"""
    artists = Artist.objects.all()
    a_art = []

    for i in artists:
      res = {}
      res['id'] = i.id
      res['name'] = i.name
      res['age'] = i.age
      res['albums'] = i.albums
      res['tracks'] = i.tracks
      res['self'] = i.self_url
      a_art.append(res)
    return Response(a_art, status=status.HTTP_200_OK)


  def retrieve(self, request, *args, **kwargs):
    """ Usado para obtener un artista"""
    params = kwargs

    try:
      artista = Artist.objects.get(id=params['id']) 
    except:
      return Response({"message": "Artista no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ArtistSerializer(artista)

    res = {}
    res['id'] = serializer.data['id']
    res['name'] = serializer.data['name']
    res['age'] = serializer.data['age']
    res['albums'] = serializer.data['albums']
    res['tracks'] = serializer.data['tracks']
    res['self'] = serializer.data['self_url']

    return Response(res, status=status.HTTP_200_OK)

  def create(self, request, *args, **kwargs):
    #revisar que entrega bien los parametros
    info = request.data  # esto me entrega name y age
    try:
      if 'name' not in info.keys():
        return Response({"message": 'Input invalido'}, status=status.HTTP_400_BAD_REQUEST)
      if 'age' not in info.keys():
        return Response({"message": 'Input invalido'}, status=status.HTTP_400_BAD_REQUEST)
      int(info['age'])
    except:
      return Response({"message": 'Input invalido'}, status=status.HTTP_400_BAD_REQUEST)

    # revisar que no exista
    encoded_id = b64encode(info['name'].encode()).decode('utf-8') [:22]
    try:
      exia = Artist.objects.get(id=encoded_id)
      serializer = ArtistSerializer(exia)

      res = {}
      res['id'] = serializer.data['id']
      res['name'] = serializer.data['name']
      res['age'] = serializer.data['age']
      res['albums'] = serializer.data['albums']
      res['tracks'] = serializer.data['tracks']
      res['self'] = serializer.data['self_url']
      return Response(res, status=status.HTTP_409_CONFLICT)
    except:
      e_album = "https://t2spotifly.herokuapp.com/artists/"
      e_album += encoded_id
      e_album += "/albums"

      e_track = "https://t2spotifly.herokuapp.com/artists/"
      e_track += encoded_id
      e_track += "/tracks"

      e_self = "https://t2spotifly.herokuapp.com/artists/"
      e_self += encoded_id

      new_artist = Artist.objects.create(name=info['name'], age=info['age'], id=encoded_id, albums=e_album, tracks=e_track, self_url=e_self)
      new_artist.save()
      serializer = ArtistSerializer(new_artist)

      res = {}
      res['id'] = serializer.data['id']
      res['name'] = serializer.data['name']
      res['age'] = serializer.data['age']
      res['albums'] = serializer.data['albums']
      res['tracks'] = serializer.data['tracks']
      res['self'] = serializer.data['self_url']

      return Response(res, status=status.HTTP_201_CREATED)

  def destroy(self, request, *args, **kwargs):
    params = kwargs
    try:
      accion = Artist.objects.get(id=params['id'])
    except:
      return Response({"message": "Artista no existe"}, status=status.HTTP_404_NOT_FOUND)
    
    accion.delete()
    return Response({"message":"artista borrado"}, status=status.HTTP_204_NO_CONTENT)

  def update(self, request, *args, **kwargs):
    artist_id = kwargs['id']
    try:
      Artist.objects.get(id=artist_id)
    except:
      return Response({"message": "Artista no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
      albums = Album.objects.filter(artist_id__id=artist_id)
      for a in albums:
        tracks = Track.objects.filter(album_id__id=a.id)

        for song in tracks:
          song.times_played += 1
          song.save()
      return Response(status=status.HTTP_200_OK)

    else:
      return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class AlbumViewset(viewsets.ModelViewSet):
  serializer_class = AlbumSerializer
  queryset = ''

  def list(self, request):
    albums = Album.objects.all()
    a_albums = []

    for i in albums:
      res = {}
      res['id'] = i.id
      res['artist_id'] = i.artist_id.id
      res['name'] = i.name
      res['genre'] = i.genre
      res['artist'] = i.artist
      res['tracks'] = i.tracks
      res['self'] = i.self_url
      a_albums.append(res)
     
    return Response(a_albums, status=status.HTTP_200_OK)

  def retrieve(self, request, *args, **kwargs):
    """ Usado para obtener un album"""
    params = kwargs

    try:
      albums = Album.objects.get(id=params['id'])
    except:
      return Response({"message": "albums no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AlbumSerializer(albums)

    res = {}
    res['id'] = serializer.data['id']
    #res['artist_id'] = serializer.data['artist_id']['id']
    res['name'] = serializer.data['name']
    res['genre'] = serializer.data['genre']
    res['artist'] = serializer.data['artist']
    res['tracks'] = serializer.data['tracks']
    res['self'] = serializer.data['self_url']
    return Response(res, status=status.HTTP_200_OK)

  def get_artist_albums(self, request, *args, **kwargs):
    params = kwargs

    try:
      a = Artist.objects.get(id=params['id'])
    except:
      return Response({"message": "Artista no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    a_id = a.id
    
    albums = Album.objects.filter(artist_id__id=a_id)
    a_albums = []

    for i in albums:
      aux_dict = {}
      aux_dict['id'] = i.id
      aux_dict['artist_id'] = i.artist_id.id
      aux_dict['name'] = i.name
      aux_dict['genre'] = i.genre
      aux_dict['artist'] = i.artist
      aux_dict['tracks'] = i.tracks
      aux_dict['self'] = i.self_url
      a_albums.append(aux_dict)
    return Response(a_albums, status=status.HTTP_200_OK)

  def create(self, request, *args, **kwargs):
    info = request.data  
    params = kwargs

    # revisar que input sea valido
    if 'name' not in info.keys():
      return Response({"message": 'Input invalido'}, status=status.HTTP_400_BAD_REQUEST)
    if 'genre' not in info.keys():
      return Response({"message": 'Input invalido'}, status=status.HTTP_400_BAD_REQUEST)

    # revisar que exista artista
    try:
      artista = Artist.objects.get(id=params['id']) 
    except:
      return Response({"message": "Artista no existe"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # revisar que no exista album
    try:
      album = Album.objects.get(name=info['name'])
      serializer = AlbumSerializer(album)

      res = {}
      res['id'] = serializer.data['id']
      res['artist_id'] = serializer.data['artist_id']['id']
      res['name'] = serializer.data['name']
      res['genre'] = serializer.data['genre']
      res['artist'] = serializer.data['artist']
      res['tracks'] = serializer.data['tracks']
      res['self'] = serializer.data['self_url']

      return Response(res, status=status.HTTP_409_CONFLICT)
    except:
      aux = info['name'] + ":" + params['id']
      e_id = b64encode(aux.encode()).decode('utf-8')[:22]

      a_artist = "https://t2spotifly.herokuapp.com/artists/" + params['id']
      a_track = "https://t2spotifly.herokuapp.com/albums/" + e_id + "/tracks"
      a_self = "https://t2spotifly.herokuapp.com/albums/" + e_id

      new_album = Album.objects.create(id=e_id, artist_id=Artist.objects.get(id=params['id']), name=info['name'], genre=info['genre'], artist=a_artist , tracks=a_track , self_url=a_self )
      new_album.save()
      serializer = AlbumSerializer(new_album)

      res = {}
      res['id'] = serializer.data['id']
      res['artist_id'] = serializer.data['artist_id']['id']
      res['name'] = serializer.data['name']
      res['genre'] = serializer.data['genre']
      res['artist'] = serializer.data['artist']
      res['tracks'] = serializer.data['tracks']
      res['self'] = serializer.data['self_url']
      return Response(res, status=status.HTTP_201_CREATED)

  def destroy(self, request, *args, **kwargs):
    params = kwargs
    try:
      accion = Album.objects.get(id=params['id'])
    except:
      return Response({"message": "Album no existe"}, status=status.HTTP_404_NOT_FOUND)
    
    accion.delete()
    return Response({"message":"Album borrado"}, status=status.HTTP_204_NO_CONTENT)

  def update(self, request, *args, **kwargs):
    album_id = kwargs['id']
    try:
      Album.objects.get(id=album_id)
    except:
      return Response({"message": "Album no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
      tracks = Track.objects.filter(album_id__id=album_id)

      for song in tracks:
        song.times_played += 1
        song.save()

      return Response(status=status.HTTP_200_OK)

    else:
      return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TrackViewset(viewsets.ModelViewSet):
  serializer_class = TrackSerializer
  queryset = ''

  def list(self, request):
    tracks = Track.objects.all()
    a_tracks = []

    for i in tracks:
      res = {}
      res['id'] = i.id
      res['album_id'] = i.album_id.id
      res['name'] = i.name
      res['duration'] = i.duration
      res['times_played'] = i.times_played
      res['artist'] = i.artist
      res['album'] = i.album
      res['self'] = i.self_url
      a_tracks.append(res)
    return Response(a_tracks, status=status.HTTP_200_OK)

  def retrieve(self, request, *args, **kwargs):
    params = kwargs

    try:
      tracks = Track.objects.get(id=params['id'])
    except:
      return Response({"message": "Tracks no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TrackSerializer(tracks)

    res = {}
    res['id'] = serializer.data['id']
    res['album_id'] = serializer.data['album_id']['id']
    res['name'] = serializer.data['name']
    res['duration'] = serializer.data['duration']
    res['times_played'] = serializer.data['times_played']
    res['artist'] = serializer.data['artist']
    res['album'] = serializer.data['album']
    res['self'] = serializer.data['self_url']

    return Response(res, status=status.HTTP_200_OK)

  def create(self, request, *args, **kwargs):
    info = request.data  
    params = kwargs

    # Revisar input invalido
    try:
      if 'name' not in info.keys():
        return Response({"message": 'Input invalido'}, status=status.HTTP_400_BAD_REQUEST)
      if 'duration' not in info.keys():
        return Response({"message": 'Input invalido'}, status=status.HTTP_400_BAD_REQUEST)
      float(info['duration'])
    except:
      return Response({"message": 'Input invalido'}, status=status.HTTP_400_BAD_REQUEST)

    # revisar que exista album
    try:
      album = Album.objects.get(id=params['id']) 
    except:
      return Response({"message": "Album no existe"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # Revisar que no exista cancion
    try:
      track = Track.objects.get(name=info['name'])

      serializer = TrackSerializer(track)

      res = {}
      res['id'] = serializer.data['id']
      res['album_id'] = serializer.data['album_id']['id']
      res['name'] = serializer.data['name']
      res['duration'] = serializer.data['duration']
      res['times_played'] = serializer.data['times_played']
      res['artist'] = serializer.data['artist']
      res['album'] = serializer.data['album']
      res['self'] = serializer.data['self_url']

      return Response(res, status=status.HTTP_409_CONFLICT)
    except:
      aux = info['name'] + ":" + params['id']
      e_id = b64encode(aux.encode()).decode('utf-8')[:22]

      aa = Album.objects.get(id=params['id']).artist_id.id

      a_artist = "https://t2spotifly.herokuapp.com/artists/" + aa
      a_album = "https://t2spotifly.herokuapp.com/albums/" + params['id']
      a_self = "https://t2spotifly.herokuapp.com/tracks/" + e_id

      new_track = Track.objects.create(id=e_id, album_id=Album.objects.get(id=params['id']), name=info['name'], duration=info['duration'], times_played=0, artist=a_artist, album=a_album, self_url=a_self)
      new_track.save()
      serializer = TrackSerializer(new_track)

      res = {}
      res['id'] = serializer.data['id']
      res['album_id'] = serializer.data['album_id']['id']
      res['name'] = serializer.data['name']
      res['duration'] = serializer.data['duration']
      res['times_played'] = serializer.data['times_played']
      res['artist'] = serializer.data['artist']
      res['album'] = serializer.data['album']
      res['self'] = serializer.data['self_url']

      return Response(res, status=status.HTTP_201_CREATED)

  def get_tracks_album(self, request, *args, **kwargs):
    params = kwargs

    try:
      a = Album.objects.get(id=params['id'])
    except:
      return Response({"message": "Album no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    a_id = a.id

    tracks = Track.objects.filter(album_id__id=a.id)

    a_tracks = []

    for i in tracks:
      res = {}
      res['id'] = i.id
      res['album_id'] = i.album_id.id
      res['name'] = i.name
      res['duration'] = i.duration
      res['times_played'] = i.times_played
      res['artist'] = i.artist
      res['album'] = i.album
      res['self'] = i.self_url
      a_tracks.append(res)

    return Response(a_tracks, status=status.HTTP_200_OK)

  def get_tracks_artist(self, request, *args, **kwargs):
    params = kwargs

    try:
      Artist.objects.get(id=params['id'])
    except:
      return Response({"message": "Artista no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    # obtener todos los albums del artista
    albums = Album.objects.filter(artist_id__id=params['id'])

    # recorrer los albums 
    a_tracks = []

    for a in albums:
      # obtengo las canciones

      tracks = Track.objects.filter(album_id__id=a.id)

      for i in tracks:
        res = {}
        res['id'] = i.id
        res['album_id'] = i.album_id.id
        res['name'] = i.name
        res['duration'] = i.duration
        res['times_played'] = i.times_played
        res['artist'] = i.artist
        res['album'] = i.album
        res['self'] = i.self_url
        a_tracks.append(res)

    return Response(a_tracks, status=status.HTTP_200_OK)

  def destroy(self, request, *args, **kwargs):
    params = kwargs
    try:
      accion = Track.objects.get(id=params['id'])
    except:
      return Response({"message": "Track no existe"}, status=status.HTTP_404_NOT_FOUND)
    
    accion.delete()
    return Response({"message":"Track borrado"}, status=status.HTTP_204_NO_CONTENT)

  def update(self, request, *args, **kwargs):
    track_id = kwargs['id']
    try:
      track = Track.objects.get(id=track_id)
    except:
      return Response({"message": "Cancion no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
      track.times_played += 1
      track.save()
      return Response(status=status.HTTP_200_OK)

    else:
      return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
