import json

from objects.functions_for_object import fct_get_external_urls_spotify, fct_has_images, fct_get_image_url, \
    fct_get_image, fct_get_followers_total, fct_format_followers_total


# Abstract class
class PlaylistObject:
    def __init__(self, collaborative, description, external_urls, href, id_, images, name, primary_color, public,
                 snapshot_id, type_, uri):
        self.collaborative = collaborative
        self.description = description
        self.external_urls = external_urls
        self.href = href
        self.id = id_
        self.images = images
        self.name = name
        self.owner = None
        self.primary_color = primary_color
        self.public = public
        self.snapshot_id = snapshot_id
        self.type = type_
        self.uri = uri

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=0)

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


# playlist().json
class PlaylistObject_total(PlaylistObject):
    def __init__(self, collaborative, description, external_urls, followers, href, id_, images, name,
                 primary_color, public, snapshot_id, type_, uri):
        super().__init__(collaborative, description, external_urls, href, id_, images, name,
                         primary_color, public, snapshot_id, type_, uri)
        self.followers = followers
        self.tracks = []

    def get_followers_total(self):
        return fct_get_followers_total(self.followers)

    def get_followers_total_str(self):
        return fct_format_followers_total(self.get_followers_total())


# user_playlists().json
# ATTENTION : self.tracks est ici un dictionnaire contenant uniquement les clés "href" et "total"
class PlaylistObject_user(PlaylistObject):
    def __init__(self, collaborative, description, external_urls, href, id_, images, name,
                 primary_color, public, snapshot_id, tracks, type_, uri):
        super().__init__(collaborative, description, external_urls, href, id_, images, name,
                         primary_color, public, snapshot_id, type_, uri)
        self.tracks = tracks


def generate_playlist_object(playlist):
    if "followers" in playlist:
        return PlaylistObject_total(playlist["collaborative"], playlist["description"], playlist["external_urls"],
                                    playlist["followers"], playlist["href"], playlist["id"], playlist["images"],
                                    playlist["name"], playlist["primary_color"], playlist["public"],
                                    playlist["snapshot_id"], playlist["type"], playlist["uri"])

    return PlaylistObject_user(playlist["collaborative"], playlist["description"], playlist["external_urls"],
                               playlist["href"], playlist["id"], playlist["images"], playlist["name"],
                               playlist["primary_color"], playlist["public"], playlist["snapshot_id"],
                               playlist["tracks"], playlist["type"], playlist["uri"])
