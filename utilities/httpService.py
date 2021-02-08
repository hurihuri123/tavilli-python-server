import requests


class HttpService(object):
    @staticmethod
    def post(url, data):
        return requests.post(url, data)
