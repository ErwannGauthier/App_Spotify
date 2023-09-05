import json

from objects.functions_for_object import fct_get_external_urls_spotify, fct_has_images, fct_get_image, \
    fct_get_image_url, fct_get_duration_ms_album, fct_get_duration_ms_album_into_string


# artist_albums().json
class AlbumObject:
    def __init__(self, album_group, album_type, available_markets, external_urls, href, id_, images, name,
                 release_date, release_date_precision, total_tracks, type_, uri):
        self.album_group = album_group
        self.album_type = album_type
        self.artists = []
        self.available_markets = available_markets
        self.external_urls = external_urls
        self.href = href
        self.id = id_
        self.images = images
        self.name = name
        self.release_date = release_date
        self.release_date_precision = release_date_precision
        self.total_tracks = total_tracks
        self.type = type_
        self.uri = uri

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=0)

    def is_single(self):
        return self.album_type.lower() == "single" and self.total_tracks == 1

    def get_external_urls_spotify(self):
        return fct_get_external_urls_spotify(self.external_urls)

    def has_images(self):
        return fct_has_images(self.images)

    def get_image_small(self):
        return fct_get_image(self.images, 2)

    def get_image_medium(self):
        return fct_get_image(self.images, 1)

    def get_image_large(self):
        return fct_get_image(self.images, 0)

    def get_image_url_small(self):
        return fct_get_image_url(self.images, 2)

    def get_image_url_medium(self):
        return fct_get_image_url(self.images, 1)

    def get_image_url_large(self):
        return fct_get_image_url(self.images, 0)


# albums().json
class AlbumObject_total(AlbumObject):
    def __init__(self, album_group, album_type, available_markets, copyrights,
                 external_ids, external_urls, genres, href, id_, images, label, name,
                 popularity, release_date, release_date_precision, total_tracks, type_, uri):
        super().__init__(album_group, album_type, available_markets, external_urls, href, id_, images, name,
                         release_date, release_date_precision, total_tracks, type_, uri)
        self.copyrights = copyrights
        self.external_ids = external_ids
        self.genres = genres
        self.label = label
        self.popularity = popularity
        self.tracks = []

    def toJSON(self):
        # to avoid circular reference exception
        for track in self.tracks:
            track.album = self.id
        json_str = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=0)
        for track in self.tracks:
            track.album = self
        return json_str

    def get_duration_ms(self):
        return fct_get_duration_ms_album(self.tracks)

    def get_duration_string(self):
        return fct_get_duration_ms_album_into_string(self.get_duration_ms())


# playlist().json --> tracks --> track --> album
class AlbumObject_playlist(AlbumObject):
    def __init__(self, album_group, album_type, available_markets, external_urls, href, id_, images, is_playable,
                 name, release_date, release_date_precision, total_tracks, type_, uri):
        super().__init__(album_group, album_type, available_markets, external_urls, href, id_, images, name,
                         release_date, release_date_precision, total_tracks, type_, uri)
        self.is_playable = is_playable


def generate_album_object(album):
    if "is_playable" in album:
        return AlbumObject_playlist(None, album["album_type"], album["available_markets"],
                                    album["external_urls"], album["href"], album["id"], album["images"],
                                    album["is_playable"], album["name"], album["release_date"],
                                    album["release_date_precision"], album["total_tracks"], album["type"], album["uri"])

    if "copyrights" in album:
        return AlbumObject_total(None, album["album_type"], album["available_markets"],
                                 album["copyrights"], album["external_ids"], album["external_urls"], album["genres"],
                                 album["href"], album["id"], album["images"], album["label"], album["name"],
                                 album["popularity"], album["release_date"], album["release_date_precision"],
                                 album["total_tracks"], album["type"], album["uri"])

    return AlbumObject(None, album["album_type"], album["available_markets"], album["external_urls"],
                       album["href"], album["id"], album["images"], album["name"], album["release_date"],
                       album["release_date_precision"], album["total_tracks"], album["type"], album["uri"])
