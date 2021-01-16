from algorithms.textMatch import calculateTextMatch


# TODO create class
def calculateMatch(descriptionMatch, imageMatch):
    return 100


def match(request, offer):
    description_match = calculateTextMatch(
        request.description, offer.description)

    return calculateMatch(description_match)
