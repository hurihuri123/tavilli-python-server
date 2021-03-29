import requests
from services.loggerService import LoggerService

OK_STATUS_CODE = 200


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

    @staticmethod
    def get(url):
        try:
            r = requests.get(url)
            if r.status_code != OK_STATUS_CODE:
                raise Exception(
                    "HTTP get request failed, status is : {},{}".format(r.status_code, r.reason))
            return r.content
        except Exception as e:
            LoggerService.error("Get request to {} failed with: {}".format(
                url, e))
            return None
