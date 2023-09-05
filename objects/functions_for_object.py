def fct_get_external_urls_spotify(external_urls):
    return external_urls["spotify"]


def fct_get_followers_total(followers):
    return followers["total"]


def fct_format_followers_total(followers_total):
    return followers_total[:len(followers_total) % 3] + ' ' + ' '.join(
        followers_total[i: i + 3] for i in range(len(followers_total) % 3, len(followers_total), 3))


def fct_has_images(images):
    return images != [] and images is not None


def fct_get_image(images, index):
    if not fct_has_images(images) or len(images) < index + 1:
        return None
    return images[index]


def fct_get_image_url(images, index):
    image = fct_get_image(images, index)
    if image is None:
        return None
    return image["url"]


def fct_get_duration_ms_album(tracks):
    duration_ms = 0
    for track in tracks:
        duration_ms += track.duration_ms
    return duration_ms

def fct_get_duration_ms_into_string(duration_ms):
    seconds = round((duration_ms / 1000) % 60)
    minutes = int((duration_ms / (1000 * 60)) % 60)
    if seconds < 10:
        seconds = "0" + str(seconds)
    elif seconds == 60:
        seconds = "00"
        minutes += 1
    return f"{minutes}:{seconds}"


def fct_get_duration_ms_album_into_string(duration_ms):
    seconds = round((duration_ms / 1000) % 60)
    minutes = int((duration_ms / (1000 * 60)) % 60)
    heures = int((duration_ms / (1000 * 60 * 60)) % 60)
    if seconds < 10:
        seconds = "0" + str(seconds)
    elif seconds == 60:
        seconds = "00"
        minutes += 1

    if minutes < 10:
        minutes = "0" + str(minutes)
    if minutes == 60:
        minutes = "00"
        heures += 1

    res = str()
    if heures == 0:
        res = f"{minutes} min {seconds} s"
    else:
        res = f"{heures} h {minutes} min"

    return res
