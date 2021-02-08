import requests


class HttpService(object):
    @staticmethod
    def post(url, json_data):
        return requests.post(url, json_data)
