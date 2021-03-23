import requests
from services.loggerService import LoggerService


class HttpService(object):
    @staticmethod
    def post(url, data):
        try:
            r = requests.post(url, json=data)
            LoggerService.debug("Post request to {} response with: {}, {}".format(
                url, r.status_code, r.reason))
            return r
        except Exception as e:
            LoggerService.error("Post request to {} failed with: {}".format(
                url, e))
            return None
