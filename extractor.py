import sys
from apis.apis import GoogleAPI, YelpAPI, InegiAPI, GenericAPI, Crawler
from general.log import logger

# SUMMARY: Class to implement a factory pattern to 
#     return the instance of an object inherited from the Connector
class ConnectorFactory(object):
    
    # Constants with values to differentiate the object to build
    GOOGLE_API = 0
    YELP_API = 1
    INEGI_API = 2
    GENERIC_API = 3
    CRAWLER = 4

    # SUMMARY: Static method that get an object instance to consult data
    # PARAM source: Value of resource to build 
    # RETURNS: Object instance that inherited from Connector class
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