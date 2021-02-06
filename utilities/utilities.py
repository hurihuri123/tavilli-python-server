from io import BytesIO
import requests
import numpy as np


def get_image_from_url(url):
    r = requests.get(url)
    return BytesIO(r.content)


def round_float_number(num):
    return int(round(num))


def list_to_nparray(l):
    return np.array(l)
