from fuzzywuzzy import fuzz


def calculateTextMatch(text1, text2):
    return fuzz.token_set_ratio(text1, text2)
