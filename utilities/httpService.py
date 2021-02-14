import requests


class HttpService(object):
    @staticmethod
    def post(url, data):
        r = requests.post(url, json=data)
        print("Post request to {} response with: {}, {}".format(
            url, r.status_code, r.reason))
        return r
