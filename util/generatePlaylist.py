import time
import urllib.request

from objects.Album import generate_album_object
from objects.Artist import generate_artist_object
from objects.Track import generate_track_object


def download_cover(url, name):
    urllib.request.urlretrieve(url, name)


def isArtistInTrack(track, artist_uri):
    present = False
    for artist in track.artists:
        if artist.uri == artist_uri:
            present = True
            break

    return present


def isTrackAlreadyFound(track, tracks):
    present = False
    for tr in tracks:
        # Comparer le nombre d'artistes
        if len(track.artists) == len(tr.artists):
            # Trier la liste des artistes
            track_artists_id = []
            tr_artists_id = []
            for i in range(len(track.artists)):
                track_artists_id.append(track.artists[i].id)
                tr_artists_id.append(tr.artists[i].id)

            # Comparer les artistes
            # Comparer le name et la duration_ms
            if track_artists_id.sort() == tr_artists_id.sort() and track.name == tr.name and track.duration_ms == tr.duration_ms:
                present = True
                break

    return present


def add_tracks_to_playlist(spotify, playlist, tracks_uri):
    if len(tracks_uri) > 100:
        for i in range(int(len(tracks_uri) / 100) + 1):
            min = 100 * i
            max = 100 * (i + 1)
            if max > len(tracks_uri):
                max = len(tracks_uri)

            spotify.playlist_add_items(playlist['id'], tracks_uri[min:max])
    else:
        spotify.playlist_add_items(playlist['id'], tracks_uri)


def generatePlaylist(spotify, artist_uri, playlist_name, playlist_description):
    time_debut = time.perf_counter()
    the_artist = generate_artist_object(spotify.artist(artist_uri))
    # Recupere tous les albums / singles / feats / compilations de l'artiste
    results = spotify.artist_albums(the_artist.uri)
    albums = results["items"]
    while results["next"]:
        results = spotify.next(results)
        albums.extend(results["items"])

    time_mid = time.perf_counter()
    print(f"Albums générés en: {round(time.perf_counter() - time_debut, 3)} secondes.")

    tracks = []
    tracks_uri = []
    for alb in albums:
        # Recupere les donnees de l'album courant
        alb = spotify.album(alb['id'])
        album = generate_album_object(alb)
        for artist in alb['artists']:
            album.add_artist(generate_artist_object(artist))

        for tr in alb["tracks"]["items"]:
            track = generate_track_object(tr, album)

            for artist in tr['artists']:
                track.add_artist(generate_artist_object(artist))

            album.add_track(track)

        # Ne prends pas les compilations, car il n'y a pas de nouveaux tracks dessus que du reposting
        if album.album_type.lower() != "compilation":
            # Parcours chaque track de l'album
            for track in album.tracks:
                # Verifie la presence de l'artiste dans le track courant
                if isArtistInTrack(track, the_artist.uri):
                    if len(tracks) == 0:
                        tracks.append(track)
                        tracks_uri.append(track.uri)
                    elif not isTrackAlreadyFound(track, tracks):
                        tracks.append(track)
                        tracks_uri.append(track.uri)

    for track in tracks:
        print(f'{track.id} - {track.name}')
    print(tracks)
    print(f"{len(tracks)} tracks.")
    print(f"Tracks générés en: {round(time.perf_counter() - time_mid, 3)} secondes.")
    print(f"Total: {round(time.perf_counter() - time_debut, 3)} secondes.")

    playlist = spotify.user_playlist_create(user=spotify.me()['id'], name=playlist_name, public=False,
                                            description=playlist_description)
    """download_cover(the_artist.images[0]['url'], "cover.jpeg")
    with open("cover.jpeg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    spotify.playlist_upload_cover_image(playlist['id'], encoded_string)"""
    add_tracks_to_playlist(spotify, playlist, tracks_uri)

    return tracks
