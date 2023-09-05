from math import ceil

from objects.Album import generate_album_object
from objects.Artist import generate_artist_object
from objects.Playlist import generate_playlist_object
from objects.Track import generate_track_object, generate_playlistTrack_object
from objects.User import generate_user_object


def create_user_playlist(spotify, name, description, public, collaborative):
    current_user = generate_user_object(spotify.me())
    playlist_data = spotify.user_playlist_create(current_user.id, name, public=public, collaborative=collaborative,
                                                 description=description)
    playlist = generate_playlist_object(playlist_data)
    owner = generate_user_object(playlist_data["owner"])
    playlist.owner = owner
    return playlist


def add_tracks_to_playlist(spotify, playlist_id, ids):
    tracks_ids = get_list_of_list_of_n_size(ids, 20)
    for tracks_id in tracks_ids:
        spotify.playlist_add_items(playlist_id, tracks_id)


def add_tracks_to_selected_playlist(spotify, ids, playlist_id, is_double):
    if is_double:
        add_tracks_to_playlist(spotify, playlist_id, ids)
    else:
        playlist = generate_playlist_and_tracks_object(spotify, [playlist_id])[0]
        # Delete
        for playlist_track in playlist.tracks:
            for id in ids:
                if playlist_track.track.id == id:
                    ids.remove(id)
                    break

        tracks_ids = get_list_of_list_of_n_size(ids, 20)
        for tracks_id in tracks_ids:
            spotify.playlist_add_items(playlist_id, tracks_id)


def convert_into_list_of_Artist(arts):
    artists = list()
    for art in arts:
        artist = generate_artist_object(art)
        artists.append(artist)
    return artists


def track_list_dict_to_track_list(track_list_dict):
    values = list(track_list_dict.values())
    result = list()
    for v in values:
        result.extend(v)
    return result


def get_current_user_playlists_object(spotify):
    results = spotify.current_user_playlists()
    playlists_data = get_items_from_dict(spotify, results)

    playlists = list()
    for pl in playlists_data:
        playlist = generate_playlist_object(pl)
        owner = generate_user_object(pl["owner"])
        playlist.owner = owner
        playlists.append(playlist)

    return playlists


def get_current_user_playlists_modifiable_object(spotify, playlists):
    current_user = generate_user_object(spotify.me())

    user_playlists = list()
    for playlist in playlists:
        if playlist.collaborative or playlist.owner.id == current_user.id:
            user_playlists.append(playlist)

    return user_playlists


def get_json_of_playlists_object(playlists):
    playlists_json = list()
    for playlist in playlists:
        playlists_json.append(playlist.toJSON())

    return playlists_json


def get_items_from_dict(spotify, dictionary):
    data = dictionary["items"]
    while dictionary["next"]:
        dictionary = spotify.next(dictionary)
        data.extend(dictionary["items"])
    return data


def get_albums_id_except_compilations(spotify, artist_id):
    # Obligé de diviser l'appel en 3 parties, car certaines fois, on obtenait dict["items"] = [] alors qu'il ne devait pas être vide
    result_album = spotify.artist_albums(artist_id, album_type='album', limit=50)
    albums = get_items_from_dict(spotify, result_album)

    result_single = spotify.artist_albums(artist_id, album_type='single', limit=50)
    albums.extend(get_items_from_dict(spotify, result_single))

    result_appears_on = spotify.artist_albums(artist_id, album_type='appears_on', limit=50)
    albums.extend(get_items_from_dict(spotify, result_appears_on))

    albums_id = list()
    for album in albums:
        if album["album_type"].lower() != "compilation":
            albums_id.append(album["id"])

    return albums_id


def get_album_tracks_where_artist_is(artist, album):
    result = list()
    for track in album.tracks:
        for art in track.artists:
            if artist.__eq__(art):
                result.append(track)
                break

    return result


def get_artist_and_other_albums(artist, albums):
    artist_albums = list()
    other_albums = list()
    for album in albums:
        if is_artist_album(artist, album):
            artist_albums.append(album)
        else:
            other_albums.append(album)

    return artist_albums, other_albums


def get_list_of_list_of_n_size(base_list, size):
    result_list = list()
    min = 0
    max = size
    for i in range(ceil(len(base_list) / size)):
        if max > len(base_list):
            max = len(base_list)
        result_list.append(base_list[min:max])
        min += size
        max += size

    return result_list


def generate_album_and_tracks_object(spotify, albums_id):
    albums_id = get_list_of_list_of_n_size(albums_id, 20)

    # Get albums data
    albums_data = list()
    for list_of_id in albums_id:
        albums_data.extend(spotify.albums(list_of_id)["albums"])

    album_objects = list()
    for album_data in albums_data:
        # Get album object
        album = generate_album_object(album_data)

        # Get artist objects
        for artist_data in album_data["artists"]:
            album.artists.append(generate_artist_object(artist_data))

        # Get tracks data
        tracks_data = album_data["tracks"]["items"]
        while album_data["tracks"]["next"]:
            album_data["tracks"] = spotify.next(album_data["tracks"])
            tracks_data.extend(album_data["tracks"]["items"])

        # Get track objects
        for track_data in tracks_data:
            track = generate_track_object(track_data)
            track.album = album
            for artist_data in track_data["artists"]:
                track.artists.append(generate_artist_object(artist_data))
            album.tracks.append(track)

        album_objects.append(album)

    return album_objects


def generate_playlist_and_tracks_object(spotify, playlists_id):
    # Get playlists data
    playlists_data = list()
    for playlist_id in playlists_id:
        playlists_data.extend([spotify.playlist(playlist_id)])

    playlist_objects = list()
    for playlist_data in playlists_data:
        # Get playlist object
        playlist = generate_playlist_object(playlist_data)

        # Get user object
        owner = generate_user_object(playlist_data["owner"])
        playlist.owner = owner

        # Get tracks data
        tracks_data = get_items_from_dict(spotify, playlist_data["tracks"])

        # Get track objects
        for track_data in tracks_data:
            playlistTrack = generate_playlistTrack_object(track_data)
            album = generate_album_object(track_data["track"]["album"])
            track = generate_track_object(track_data["track"])
            track.album = album
            for artist_data in track_data["track"]["artists"]:
                track.artists.append(generate_artist_object(artist_data))
            playlistTrack.track = track
            playlist.tracks.append(playlistTrack)

        playlist_objects.append(playlist)

    return playlist_objects


def generate_track_list(artist, albums):
    track_list = dict()

    for album in albums:
        for track in album.tracks:
            if track.is_track_of_artist(artist):
                key = track.get_duration_string()
                if key in track_list.keys():
                    is_track_in_track_list(track_list[key], track)
                    track_list[key].append(track)
                else:
                    track_list[key] = [track]

    return track_list


def generate_track_list_sorted(artist, artist_albums, other_albums):
    track_list_sorted = list()

    for album in artist_albums:
        for track in album.tracks:
            if track.is_track_of_artist(artist):
                track_list_sorted.append(track)

    for album in other_albums:
        for track in album.tracks:
            if track.is_track_of_artist(artist):
                track_list_sorted.append(track)

    return track_list_sorted


def is_artist_album(artist, album):
    result = False
    if album.album_type.lower() == "album":
        for art in album.artists:
            if artist.__eq__(art):
                result = True
                break

    return result


def is_track_in_track_list(track_list, track):
    result = False

    for tr in track_list:
        result = False
        if tr.id == track.id:
            print(f"Track name : {track.name} {track.album.name}\n"
                  f"tr name : {tr.name}")
            result = True
        elif (track.name in tr.name or tr.name in track.name) and len(track.artists) == len(tr.artists):
            # Sort artists list
            track_artists_id = list()
            tr_artists_id = list()
            for i in range(len(track.artists)):
                track_artists_id.append(track.artists[i].id)
                tr_artists_id.append(tr.artists[i].id)

            # If list are the same, result = True
            if track_artists_id.sort() == tr_artists_id.sort():
                result = True

        if result:
            def set_is_copy_true(t):
                t.is_copy = True

            if track.album.is_single() and not tr.album.is_single():
                set_is_copy_true(track)
            elif not track.album.is_single() and tr.album.is_single():
                set_is_copy_true(tr)
            else:
                if track.album.release_date > tr.album.release_date:
                    set_is_copy_true(track)
                else:
                    set_is_copy_true(tr)

    return result
