import json
import time

import utilities.sslCertificate

from config.config import *
from services.httpServer import HttpServer
from http.server import BaseHTTPRequestHandler, HTTPServer
from utilities.tavilliAPI import TavilliAPI, API_MATCHES_FIELD
from utilities.httpService import HttpService
from services.loggerService import LoggerService
from utilities.utilities import json_to_bytes
from utilities.queries import Queries, OFFERS_TABLE, REQUESTS_TABLE, MATCH_FIELDS, CATEGORY_FIELD, SUBCATEGORY_FIELD, Offer, Request, REQUEST_OBJECT_NAME, OFFER_OBJECT_NAME
from utilities.mailTemplates import *
from services.mailService import MailService
from services.matcherService import MatcherService


class WebServerHandler(BaseHTTPRequestHandler):
    matcher = None
    mailSender = None

    @classmethod
    def post_start(cls):
        LoggerService.info("Initializing objects...")
        cls.matcher = MatcherService()
        cls.mailSender = MailService(SERVICE_MAIL, SERVICE_MAIL_PASSWORD)

    def do_POST(self):
        route = self.path
        body = self.parseJsonBody()

        if route == "/newRequest":
            # Search for matches
            self.handle_new_item(item_id=body["requestId"], object_type=Request,
                                 select_query=Queries.getRequestById, search_matches_callback=self.matcher.search_matches_for_request)
            # Notify relevent suppliers about new request
            request_url = body["requestUrl"]
            relevent_suppliers = body["mailTo"]
            if request_url and relevent_suppliers:
                for supplier_info in relevent_suppliers:
                    self.mailSender.send_email(
                        destinationMail=supplier_info["email"], subject=NEW_RELEVENT_MAIL_TITLE, email_body=new_relevent_template(request_url))
                LoggerService.debug("Sent {} to relevent suppliers".format(
                    len(relevent_suppliers)))

        elif route == "/newSupplierProduct":
            self.handle_new_item(item_id=body["offerId"], object_type=Offer,
                                 select_query=Queries.getOfferById, search_matches_callback=self.matcher.search_matches_for_offer)
        elif route == "/itemsDeleted":
            items = body["items"]
            if items is None or isinstance(items, list) == False:
                return self.badRequestResponse()

            for item in items:
                if "type" not in item or "id" not in item:
                    return self.badRequestResponse()
                item_type = item["type"]
                item_id = item["id"]

                if item_type == REQUEST_OBJECT_NAME:
                    # Perform delete of request object
                    items = self.matcher.database.executeQuery(
                        Queries.getRequestById(item_id))
                    if items is None or len(items) != 1:
                        return self.notFoundResponse()
                    try:
                        item = Request(items[0])
                        self.matcher.delete_item_images(item=item,
                                                        items_directory_path=self.matcher.requests_directory)
                    except Exception as e:
                        LoggerService.error(
                            "Error in delete images of request: {}".format(e))
                        return self.internalErrResponse()

                elif item_type == OFFER_OBJECT_NAME:
                    # Perform delete of offer object
                    items = self.matcher.database.executeQuery(
                        Queries.getOfferById(item_id))
                    if items is None or len(items) != 1:
                        return self.notFoundResponse()
                    try:
                        item = Offer(items[0])
                        self.matcher.delete_item_images(item=item,
                                                        items_directory_path=self.matcher.offers_directory)
                    except Exception as e:
                        LoggerService.error(
                            "Error in delete images of offer: {}".format(e))
                        return self.internalErrResponse()

                else:
                    return self.badRequestResponse()
            self.successResponse()

        else:
            LoggerService.debug("Receive new POST with unknown route")
            self.notFoundResponse()

    def handle_new_item(self, item_id, object_type, select_query, search_matches_callback):
        if item_id is None:
            return self.badRequestResponse()
        # Select request from DB
        items = self.matcher.database.executeQuery(
            select_query(item_id))
        if items is None or len(items) != 1:
            # Sleep and try reading item again - probably node's insert query changes aren't updated yet
            time.sleep(2)
            # Second read attempt
            items = self.matcher.database.executeQuery(
                select_query(item_id))
            if items is None or len(items) != 1:
                LoggerService.error(
                    "Item with ID {} was not found".format(item_id))
                return self.notFoundResponse()
        # Search matches for item
        try:
            item = object_type(items[0])
            matches = search_matches_callback(item)
            response = TavilliAPI.requestMatchesResponse(matches)
            self.successResponse(response)
        except Exception as e:
            LoggerService.error("Error in handle new item: {}".format(e))
            self.internalErrResponse()

        # ----------- Helpers -----------

    def parseJsonBody(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')
        return json.loads(body) if body else None

    def sendJsonHeaders(self):
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

# ----------- Responses -----------
        """
        Args:
        Returns:
            VOID
        """

    def successResponse(self, json_data=None):
        self.send_response(200)
        self.sendJsonHeaders()
        if json_data:
            self.wfile.write(json_to_bytes(json_data))

    def badRequestResponse(self):
        self.send_response(400)
        self.sendJsonHeaders()

    def notFoundResponse(self):
        self.send_response(404)
        self.sendJsonHeaders()

    def internalErrResponse(self):
        self.send_response(500)
        self.sendJsonHeaders()


if __name__ == "__main__":
    HttpServer(web_server_handler=WebServerHandler).listen(8000)
