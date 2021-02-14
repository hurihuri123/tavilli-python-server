from io import BytesIO
import requests
import json


def get_image_from_url(url):
    r = requests.get(url)
    return BytesIO(r.content)


def round_float_number(num):
    return int(round(num))


def json_to_bytes(json_data):
    return json.dumps(
        json_data).encode('utf-8')
