from io import BytesIO
import requests


def get_image_from_url(url):
    r = requests.get(url)
    return BytesIO(r.content)
