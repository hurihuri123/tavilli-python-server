from collections import defaultdict

REQUEST_ID_FIELD = "requestId"

TAVILLI_API_SUCCESS_FIELD = "success"
TAVILLI_API_MATCHES_FIELD = "matches"
TAVILLI_API_ERROR_FIELD = "error"


class TavilliAPI():
    """
        Args:
        Returns:
            json wth array of matches grouped by request id
            For example:
            {data:[{'matches': [...], 'requestId': 9}, {'matches': [...], 'requestId': 8}, {'matches': [...], 'requestId': 7}]}
    """
    @staticmethod
    def newMatchesHttpRequest(matches):
        result = []
        group_by_request = {}
        for match in matches:
            try:
                len(group_by_request[match.request.id])
            except:
                group_by_request[match.request.id] = []
            finally:
                match_json = match.__str__()
                # Avoid duplications
                if match_json not in group_by_request[match.request.id]:
                    group_by_request[match.request.id].append(match_json)

        for request_id, request_matches in group_by_request.items():
            item = {}
            item[REQUEST_ID_FIELD] = request_id
            item[TAVILLI_API_MATCHES_FIELD] = request_matches
            result.append(item)
        return {"data": result}

    @staticmethod
    def requestMatchesResponse(matches):
        mappedMatches = []
        for match in matches:
            mappedMatches.append(match.__str__())

        return mappedMatches
