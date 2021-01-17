from utilities.mySql import MySqlConnector
from utilities.queries import Queries, OFFERS_TABLE, REQUESTS_TABLE, MATCH_FIELDS
from algorithms.match import Match
from config.config import *

if __name__ == "__main__":
    database = MySqlConnector(
        DATABASE_HOST, DATABASE_USERNAME, DATEBASE_PASSWORD, DATABASE_NAME)
    offers = database.executeQuery(Queries.getOffers())
    requests = database.executeQuery(Queries.getRequests())
    matches = []

    for request in requests:
        for offer in offers:
            match = Match(request, offer)
            if(match.calculate() > 70):
                matches.append(match)

    for match in matches:
        print(match)
