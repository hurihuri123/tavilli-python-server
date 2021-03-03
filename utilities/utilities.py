from io import BytesIO
import requests
import json


def get_image_from_url(url):
    r = requests.get(url)
    return BytesIO(r.content)


def round_float_number(num):
    return int(round(num))


# Calculate how many percentage the bigger number is bigger than the lower number
def distance_percentage(num1, num2):
    if num1 >= num2:
        big = num1
        low = num2
    else:
        big = num2
        low = num1
    try:
        return ((big / low) * 100.0) - 100
    except ZeroDivisionError:
        return None


def json_to_bytes(json_data):
    return json.dumps(
        json_data).encode('utf-8')
