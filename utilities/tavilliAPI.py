MATCHES_FIELD = "matches"
REQUEST_ID_FIELD = "requestId"


class TavilliAPI():
    @staticmethod
    def requestMatchesResponse(request, matches):
        result = {}
        result[REQUEST_ID_FIELD] = request.id
        result[MATCHES_FIELD] = []
        for match in matches:
            result[MATCHES_FIELD].append(match.__str__())

        return result
