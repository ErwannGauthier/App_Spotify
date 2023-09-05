# https://github.com/plamere/spotipy/blob/master/examples/app.py

import os
import time

import spotipy
from dotenv import load_dotenv
from flask import Flask, render_template, url_for, redirect, session, request, jsonify
from flask_session import Session
from spotipy.oauth2 import SpotifyOAuth

from objects.Artist import generate_artist_object
from util.functions import convert_into_list_of_Artist, generate_album_and_tracks_object, \
    get_albums_id_except_compilations, generate_track_list, track_list_dict_to_track_list, get_artist_and_other_albums, \
    generate_track_list_sorted, generate_playlist_and_tracks_object, get_current_user_playlists_object, \
    get_current_user_playlists_modifiable_object, get_json_of_playlists_object, create_user_playlist, \
    add_tracks_to_playlist, add_tracks_to_selected_playlist
from util.generatePlaylist import generatePlaylist

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

load_dotenv(dotenv_path="config")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SCOPE = 'user-library-read playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public'
CACHE_HANDLER = spotipy.cache_handler.FlaskSessionCacheHandler(session)


def get_auth_manager():
    return SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=url_for('login', _external=True),
                        scope=SCOPE, cache_handler=CACHE_HANDLER, show_dialog=True)


@app.route('/')
def index():
    auth_manager = get_auth_manager()
    context = dict()

    # Step 1. Redirect to login page when no token
    if not auth_manager.validate_token(CACHE_HANDLER.get_cached_token()):
        return redirect(url_for('login', _external=True))

    spotify = spotipy.Spotify(auth_manager=auth_manager)

    # print(spotify.current_user_playlists())
    # print(spotify.playlist("0MxLONZxmFxd8yK9WwI6kt"))

    playlists = get_current_user_playlists_object(spotify)

    context['playlists'] = playlists

    context['username'] = spotify.me()["display_name"]

    return render_template('index.html', context=context)


@app.route('/login')
def login():
    auth_manager = get_auth_manager()

    # If user is already logged in --> redirection index
    if auth_manager.validate_token(CACHE_HANDLER.get_cached_token()):
        return redirect(url_for('/', _external=True))

    # Step 2. Being redirected from Spotify auth page
    if request.args.get("code"):
        auth_manager.get_access_token(request.args.get("code"))
        return redirect(url_for('/', _external=True))

    return redirect(auth_manager.get_authorize_url())


@app.route('/logout')
def logout():
    session.pop("token_info", None)
    return redirect(url_for('/', _external=True))


@app.route('/playlistGenerator', methods=['GET', 'POST'])
def playlistGenerator():
    auth_manager = get_auth_manager()
    context = dict()

    # Step 1. Redirect to login page when no token
    if not auth_manager.validate_token(CACHE_HANDLER.get_cached_token()):
        return redirect(url_for('login', _external=True))

    spotify = spotipy.Spotify(auth_manager=auth_manager)

    query = request.args.get('query')
    if query is not None and query != "":
        search = spotify.search(q=query, type='artist', limit=50)
        context['artists'] = convert_into_list_of_Artist(search['artists']['items'])

    if request.form.get('artistURI') and request.form.get('playlistName'):
        artist_uri = request.form.get('artistURI')
        playlist_name = request.form.get('playlistName')
        playlist_description = ""
        if request.form.get('playlistDescription'):
            playlist_description = request.form.get('playlistDescription')
        generatePlaylist(spotify, artist_uri, playlist_name, playlist_description)

    return render_template('playlistGenerator.html', context=context)


@app.route('/artist/<artist_id>', methods=['GET', 'POST'])
def artist_data(artist_id):
    auth_manager = get_auth_manager()
    context = dict()

    # Step 1. Redirect to login page when no token
    if not auth_manager.validate_token(CACHE_HANDLER.get_cached_token()):
        return redirect(url_for('login', _external=True))

    spotify = spotipy.Spotify(auth_manager=auth_manager)

    start = time.time()
    actual = start

    # Get the artist data
    artist = generate_artist_object(spotify.artist(artist_id))
    print(f"Get artist data : {time.time() - actual}")
    actual = time.time()

    # Get albums id where the artist is present
    albums_id = get_albums_id_except_compilations(spotify, artist_id)
    print(f"Get albums id : {time.time() - actual}")
    actual = time.time()

    # Get albums data
    albums = generate_album_and_tracks_object(spotify, albums_id)
    print(f"Get album data : {time.time() - actual}")
    actual = time.time()

    # Get artist albums and other albums
    artist_albums, other_albums = get_artist_and_other_albums(artist, albums)
    print(f"Get artist albums and other albums : {time.time() - actual}")
    actual = time.time()

    # Get track list
    track_list_dict = generate_track_list(artist, albums)
    track_list = track_list_dict_to_track_list(track_list_dict)
    track_list_sorted = generate_track_list_sorted(artist, artist_albums, other_albums)
    print(f"Get track list : {time.time() - actual}")
    actual = time.time()

    print(f"Total : {actual - start}")

    context['artist'] = artist
    context['artist_albums'] = artist_albums
    context['other_albums'] = other_albums
    context['tracks'] = track_list_sorted

    return render_template('artist_data.html', context=context)


@app.route('/album/<album_id>', methods=['GET', 'POST'])
def album_data(album_id):
    auth_manager = get_auth_manager()
    context = dict()

    # Step 1. Redirect to login page when no token
    if not auth_manager.validate_token(CACHE_HANDLER.get_cached_token()):
        return redirect(url_for('login', _external=True))

    spotify = spotipy.Spotify(auth_manager=auth_manager)

    album = generate_album_and_tracks_object(spotify, [album_id])[0]

    context["album"] = album

    return render_template('album_data.html', context=context)


@app.route('/playlist/<playlist_id>')
def playlist_data(playlist_id):
    auth_manager = get_auth_manager()
    context = dict()

    # Step 1. Redirect to login page when no token
    if not auth_manager.validate_token(CACHE_HANDLER.get_cached_token()):
        return redirect(url_for('login', _external=True))

    spotify = spotipy.Spotify(auth_manager=auth_manager)

    playlist = generate_playlist_and_tracks_object(spotify, [playlist_id])[0]

    context["playlist"] = playlist

    return render_template('playlist_data.html', context=context)


@app.route('/get_playlists', methods=['POST'])
def get_playlists():
    auth_manager = get_auth_manager()
    context = dict()

    # Step 1. Redirect to login page when no token
    if not auth_manager.validate_token(CACHE_HANDLER.get_cached_token()):
        return redirect(url_for('login', _external=True))

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    playlists = get_current_user_playlists_object(spotify)
    user_playlists = get_current_user_playlists_modifiable_object(spotify, playlists)
    user_playlists_json = get_json_of_playlists_object(user_playlists)

    context["playlists"] = user_playlists_json

    return jsonify(context)


@app.route('/create_new_playlist', methods=['POST'])
def create_new_playlist():
    auth_manager = get_auth_manager()
    context = dict()

    # Step 1. Redirect to login page when no token
    if not auth_manager.validate_token(CACHE_HANDLER.get_cached_token()):
        return redirect(url_for('login', _external=True))

    spotify = spotipy.Spotify(auth_manager=auth_manager)

    if request.json["name"] != "" and len(request.json["ids"]) > 0 and not (
            request.json["collaborative"] is True and request.json["public"] is True):
        name = request.json["name"]
        description = request.json["description"]
        public = request.json["public"]
        collaborative = request.json["collaborative"]

        playlist = create_user_playlist(spotify, name, description, public, collaborative)
        tracks_id = request.json["ids"]
        add_tracks_to_playlist(spotify, playlist.id, tracks_id)

        context["result"] = True
    else:
        context["result"] = False

    return jsonify(context)


@app.route('/add_selected_playlist', methods=['POST'])
def add_selected_playlist():
    auth_manager = get_auth_manager()
    context = dict()

    # Step 1. Redirect to login page when no token
    if not auth_manager.validate_token(CACHE_HANDLER.get_cached_token()):
        return redirect(url_for('login', _external=True))

    spotify = spotipy.Spotify(auth_manager=auth_manager)

    if len(request.json["selection"]) > 0 and len(request.json["ids"]) > 0:
        selection = request.json["selection"]
        tracks_id = request.json["ids"]

        for couple in selection:
            add_tracks_to_selected_playlist(spotify, tracks_id, couple[0], couple[1])

        context["result"] = True
    else:
        context["result"] = False

    return jsonify(context)


if __name__ == '__main__':
    app.run()
