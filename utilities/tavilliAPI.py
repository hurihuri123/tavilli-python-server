from collections import defaultdict

API_MATCHES_FIELD = "matches"
REQUEST_ID_FIELD = "requestId"


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
            item[API_MATCHES_FIELD] = request_matches
            result.append(item)
        return {"data": result}

    @staticmethod
    def requestMatchesResponse(request, matches):
        result = {}
        result[REQUEST_ID_FIELD] = request.id
        result[API_MATCHES_FIELD] = []
        for match in matches:
            result[API_MATCHES_FIELD].append(match.__str__())

        return result
