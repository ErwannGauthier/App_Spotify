import json

from objects.functions_for_object import fct_get_external_urls_spotify, fct_has_images, fct_get_image, \
    fct_get_image_url, fct_get_followers_total, fct_format_followers_total


# playlist().json --> tracks --> added_by
class UserObject:
    def __init__(self, external_urls, href, id_, type_, uri):
        self.external_urls = external_urls
        self.href = href
        self.id = id_
        self.type = type_
        self.uri = uri

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=0)

    def get_external_urls_spotify(self):
        return fct_get_external_urls_spotify(self.external_urls)


# playlist().json --> owner
# user_playlists().json --> owner
class UserObject_display_name(UserObject):
    def __init__(self, display_name, external_urls, href, id_, type_, uri):
        super().__init__(external_urls, href, id_, type_, uri)
        self.display_name = display_name


# user().json
class UserObject_total(UserObject_display_name):
    def __init__(self, display_name, external_urls, followers, href, id_, images, type_, uri):
        super().__init__(display_name, external_urls, href, id_, type_, uri)
        self.followers = followers
        self.images = images

    def get_followers_total(self):
        return fct_get_followers_total(self.followers)

    def get_followers_total_str(self):
        return fct_format_followers_total(self.get_followers_total())

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


def generate_user_object(user):
    if "images" in user:
        return UserObject_total(user["display_name"], user["external_urls"], user["followers"], user["href"],
                                user["id"], user["images"], user["type"], user["uri"])

    if "display_name" in user:
        return UserObject_display_name(user["display_name"], user["external_urls"], user["href"], user["id"],
                                       user["type"], user["uri"])

    return UserObject(user["external_urls"], user["href"], user["id"], user["type"], user["uri"])
