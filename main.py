from utilities.mySql import MySqlConnector
from utilities.queries import Queries, OFFERS_TABLE, REQUESTS_TABLE, MATCH_FIELDS, CATEGORY_FIELD, SUBCATEGORY_FIELD
from algorithms.match import Match
from config.config import *


#TODO: doc
def search_match_for_request(request):
    matches = []
    # TODO: select filter by request price as well
    # Select offers according to request info
    offers = database.executeQuery(Queries.getOffers(
        request[CATEGORY_FIELD], request[SUBCATEGORY_FIELD]))
    # Init images dataset according to request category
    # Get request's image features
    # Compare dataset with query features
    for offer in offers:
        # Find related offer matches results
        # Pass list of images matches results to match object (might be more than one image)
        match = Match(request, offer)
        if(match.matchPercantage > 70):
            matches.append(match)
    return matches


def search_match_for_offer(offer):
    pass


if __name__ == "__main__":
    database = MySqlConnector(
        DATABASE_HOST, DATABASE_USERNAME, DATEBASE_PASSWORD, DATABASE_NAME)

    requests = database.executeQuery(Queries.getRequests())
    matches = search_match_for_request()
