import sys
from apis.apis import GoogleAPI, YelpAPI, InegiAPI, GenericAPI, Crawler
from general.log import logger


class ConnectorFactory(object):
    """ Class to implement a factory pattern """
    GOOGLE_API = 0
    YELP_API = 1
    INEGI_API = 2
    GENERIC_API = 3
    CRAWLER = 4

    @staticmethod
    def get_connector(source):
        if ConnectorFactory.GOOGLE_API == source:
            return GoogleAPI()
        elif ConnectorFactory.YELP_API == source:
            return YelpAPI()
        elif ConnectorFactory.INEGI_API == source:
            return Crawler()
        elif ConnectorFactory.GENERIC_API == source:
            return InegiAPI()
        elif ConnectorFactory.CRAWLER == source:
            return Crawler()