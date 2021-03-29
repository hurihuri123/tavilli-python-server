from io import BytesIO
import requests
import json

from utilities.httpService import HttpService


def get_image_from_url(url):
    image_content = HttpService.get(url)
    return BytesIO(image_content)


def round_float_number(num):
    return int(round(num))


# Calculate how many percentage the bigger number is bigger than the lower number
# NOTE: incase of modifying this function, must update Tavilli.client similar function located at helper.ts
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
