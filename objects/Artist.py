import json

from objects.functions_for_object import fct_get_external_urls_spotify, fct_has_images, fct_get_image, \
    fct_get_image_url, fct_get_followers_total, fct_format_followers_total


# albums.json() --> artists
# albums.json() --> tracks --> artists
# artist_albums().json --> artists
# playlist().json --> tracks --> track --> artists
# playlist().json --> tracks --> track --> album --> artists
class ArtistObject:
    def __init__(self, external_urls, href, id_, name, type_, uri):
        self.external_urls = external_urls
        self.href = href
        self.id = id_
        self.name = name
        self.type = type_
        self.uri = uri

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=0)

    def get_external_urls_spotify(self):
        return fct_get_external_urls_spotify(self.external_urls)


# artist().json
class ArtistObject_total(ArtistObject):
    def __init__(self, external_urls, followers, genres, href, id_, images, name, popularity, type_, uri):
        super().__init__(external_urls, href, id_, name, type_, uri)
        self.followers = followers
        self.genres = genres
        self.images = images
        self.popularity = popularity

    def get_followers_total(self):
        return fct_get_followers_total(self.followers)

    def get_followers_total_str(self):
        return fct_format_followers_total(str(self.get_followers_total()))

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


def generate_artist_object(artist):
    if "images" in artist:
        return ArtistObject_total(artist["external_urls"], artist["followers"], artist["genres"], artist["href"],
                                  artist["id"], artist["images"], artist["name"], artist["popularity"], artist["type"],
                                  artist["uri"])

    return ArtistObject(artist["external_urls"], artist["href"], artist["id"], artist["name"], artist["type"],
                        artist["uri"])
