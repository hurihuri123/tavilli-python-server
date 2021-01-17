from utilities.mySql import MySqlConnector
from utilities.queries import Queries, OFFERS_TABLE, REQUESTS_TABLE
from algorithms.match import match
from config.config import *

if __name__ == "__main__":
    database = MySqlConnector(
        DATABASE_HOST, DATABASE_USERNAME, DATEBASE_PASSWORD, DATABASE_NAME)
    offers = database.executeQuery(Queries.getOffers())
    requests = database.executeQuery(Queries.getRequests())
    matches = []
    print(database.executeQuery(Queries.showTableColumns(OFFERS_TABLE)))

    for request in requests:
        for offer in offers:
            matchPercentage = match(request, offer)
            if(matchPercentage > 70):
                matches.append({offer, request, matchPercentage})

    print(matches)
