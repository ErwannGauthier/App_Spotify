import json

from objects.functions_for_object import fct_get_external_urls_spotify, fct_get_duration_ms_into_string


# albums.json() --> tracks
class TrackObject:
    def __init__(self, available_markets, disc_number, duration_ms, explicit,
                 external_urls, href, id_, is_local, name, preview_url, track_number,
                 type_, uri):
        self.album = None
        self.artists = []
        self.available_markets = available_markets
        self.disc_number = disc_number
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.external_urls = external_urls
        self.href = href
        self.id = id_
        self.is_local = is_local
        self.name = name
        self.preview_url = preview_url
        self.track_number = track_number
        self.type = type_
        self.uri = uri

    def toJSON(self):
        # to avoid circular reference exception
        tempo = self.album
        self.album = self.album.id
        json_str = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=0)
        self.album = tempo
        return json_str

    def is_featuring(self):
        return len(self.artists) > 1

    def is_album_of_artist(self, artist):
        return self.album.album_type.lower() == "album" and artist in self.album.artists

    def is_track_of_artist(self, artist):
        result = False
        for art in self.artists:
            if artist.id == art.id:
                result = True
                break
        return result

    def get_external_urls_spotify(self):
        return fct_get_external_urls_spotify(self.external_urls)

    def get_duration_string(self):
        return fct_get_duration_ms_into_string(self.duration_ms)


# playlist().json --> tracks --> track
# ATTENTION : self.episode et self.track sont ici des booléens
class PlaylistTracksObject_track(TrackObject):
    def __init__(self, available_markets, disc_number, duration_ms, episode, explicit, external_ids,
                 external_urls, href, id_, is_local, name, popularity, preview_url, track, track_number, type_, uri):
        super().__init__(available_markets, disc_number, duration_ms, explicit,
                         external_urls, href, id_, is_local, name, preview_url, track_number,
                         type_, uri)
        self.episode = episode
        self.external_ids = external_ids
        self.popularity = popularity
        self.track = track


# playlist().json --> tracks
class PlaylistTracksObject:
    def __init__(self, added_at, added_by, is_local, primary_color, video_thumbnail):
        self.added_at = added_at
        self.added_by = added_by
        self.is_local = is_local
        self.primary_color = primary_color
        self.track = None
        self.video_thumbnail = video_thumbnail

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=0)


def generate_track_object(track):
    if "popularity" in track:
        return PlaylistTracksObject_track(track["available_markets"], track["disc_number"], track["duration_ms"],
                                          track["episode"], track["explicit"], track["external_ids"],
                                          track["external_urls"], track["href"], track["id"], track["is_local"],
                                          track["name"], track["popularity"], track["preview_url"], track["track"],
                                          track["track_number"], track["type"], track["uri"])

    return TrackObject(track["available_markets"], track["disc_number"], track["duration_ms"], track["explicit"],
                       track["external_urls"], track["href"], track["id"], track["is_local"], track["name"],
                       track["preview_url"], track["track_number"], track["type"], track["uri"])


def generate_playlistTrack_object(playlist_track):
    return PlaylistTracksObject(playlist_track["added_at"], playlist_track["added_by"], playlist_track["is_local"],
                                playlist_track["primary_color"], playlist_track["video_thumbnail"])
