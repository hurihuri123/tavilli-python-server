import requests


class HttpService(object):
    @staticmethod
    def post(url, data):
        try:
            r = requests.post(url, json=data)
            print("Post request to {} response with: {}, {}".format(
                url, r.status_code, r.reason))
            return r
        except Exception as e:
            print("Post request to {} failed with: {}".format(
                url, e))
            return None
