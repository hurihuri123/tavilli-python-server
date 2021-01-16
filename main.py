from utilities.mySql import MySql
from utilities.queries import Queries
from algorithms.match import match

if __name__ == "__main__":
    # Get all offers related to category
    database = MySql("")
    offers = database.executeQuery(Queries.getOffers())
    requests = database.executeQuery(Queries.getRequests())
    matches = []

    for request in requests:
        for offer in offers:
            matchPercentage = match(request, offer)
            if(matchPercentage > 70):
                matches.append({offer, request, matchPercentage})

    print(matches)
