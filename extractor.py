import sys
from apis.apis import GoogleAPI, InegiAPI, GenericAPI, Crawler, YelpAPI
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
    def get_connector(source, abstract_mapper = None):
        if ConnectorFactory.GOOGLE_API == source:
            if abstract_mapper != None:
                return GoogleAPI(abstract_mapper)
            else:
                return GoogleAPI()
        if ConnectorFactory.YELP_API == source:
            if abstract_mapper != None:
                return YelpAPI(abstract_mapper)
            else:
                return YelpAPI()
        elif ConnectorFactory.INEGI_API == source:
            if abstract_mapper != None:
                return InegiAPI(abstract_mapper)
            else:
                return InegiAPI()
        elif ConnectorFactory.GENERIC_API == source:
            if abstract_mapper != None:
                return GenericAPI(abstract_mapper)
            else:
                return GenericAPI()
        elif ConnectorFactory.CRAWLER == source:
            return Crawler()