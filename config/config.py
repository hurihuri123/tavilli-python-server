
if(True):
    DATABASE_HOST = "localhost"
    DATABASE_USERNAME = "root"
    DATEBASE_PASSWORD = ""
    DATABASE_NAME = "tavilli"

    IMAGES_HOST = "http://localhost:8443"
    API_HOST = "http://localhost:8443"
else:
    DATABASE_HOST = "database-2.cxekfsj5gkic.eu-central-1.rds.amazonaws.com"
    DATABASE_USERNAME = "admin"
    DATEBASE_PASSWORD = "tavilI123"
    DATABASE_NAME = "tavilli"

    IMAGES_HOST = "https://prod-images.tavilli.co.il"
    API_HOST = "https://prod-server.tavilli.co.il:8443"


IMAGES_FOLDER = IMAGES_HOST + "/images"
OFFERS_IMAGES_FOLDER = IMAGES_FOLDER + "/offers"
REQUESTS_IMAGES_FOLDER = IMAGES_FOLDER + "/requests"

RETRO_MATCHES_ROUTE = "/autoMatches/new"
