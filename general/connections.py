from abc import ABCMeta, abstractmethod
import requests 
import json
import sys
from .log import logger
from .Mapper import AbstractMapper, DefaultMapper
sys.path.append('./../')
from crawler.scrapper_middleware import ScrapperMiddleWare
  
# SUMMARY: Abstract class that defines the structure for the 
#     different kind of connections
class Connector(object):

    __metaclass__ = ABCMeta

    # SUMMARY: It is an abstract method that is overwritten in 
    #     the simplest implementation of the class.
    @abstractmethod 
    def consult(self):
        print('Consult method')

    # SUMMARY: It is an abstract method that is overwritten in 
    #     the simplest implementation of the class.
    @abstractmethod
    def map_out(self):
        print('Map out method')

# SUMMARY : This class inherits the methods of the connector class, 
#     and will be used to query and map out data from API's
class ConnectorAPI(Connector):

    # SUMMARY: This is an dictionary and its function is to establish the 
    #     name of the properties from which it will extract the common 
    #     information for the model
    MAP_COMMON_DATA = {
        'longitud' : '',
        'latitud' : '',
        'data' : ''
    }

    # SUMMARY: This is an dictionary and its function is to determinate 
    #     the data with a high degree of value, it is overwritten in 
    #     the implementation of the class
    METADATA = {}

    # SUMMARY: It is a property to which a class is established, 
    #     which must inherit from AbstractMapper
    mapper = AbstractMapper()

    # SUMMARY: It is an initializer that establishes a class that allows 
    #     changing the structure of the Json, you can assign it a class of 
    #     its own that it inherits from AbstractMapper, otherwise, a default 
    #     is established
    def __init__(self, url, abstract_mapper = None):
        self.url = url
        if abstract_mapper is None:
            self.mapper = DefaultMapper()
        else:
            self.mapper = abstract_mapper

    # SUMMARY:  Main method of operation, this method consults the 
    #     data to the API and also executes the method map_out() 
    #     to return a list with information of the query and has an 
    #     established format
    # RETURN: A List GeoModel with all information consulted.
    def consult(self):

        try:
            # Consult API and get a object json
            self.obj_json = Connection.api_connection(self.url)

            # The structure of the API is changed, according to the AbstractMapper
            #     class established in the creation of the instance of the class       
            listModel = self.map_out()
            
            # Return a List GeoModel
            return listModel
        except Exception as err:
            print(err)

    # SUMMARY: This executes a method that allows to change the structure of the 
    #     json object consulted, according to the mapper property that is a class 
    #     that inherits from AbstractMapper
    # RETURN: A List GeoModel with all information consulted.
    def map_out(self):
        return self.mapper.mapout_API(self.obj_json, self.MAP_COMMON_DATA, self.METADATA)


# SUMMARY: Class with diferent kind methods connection
class Connection(object):
    
    # SUMMARY: This is a static method that allows to consult data of any API
    # REMARKS: Currently does not support API query with authentication OAuth1.0,
    #     OAuth2.0 or Basic, you can only pass tokens by headers 
    # RETURN: A object json with data consulted
    @staticmethod
    def api_connection(url, params=None, headers=None, cookies=None):

        message = ''
        response = ''

        # Check if the url is empty
        if url == '':
            raise ValueError("You need execute .filter method before .consult().")

        # Try to make the query
        try:
            response = requests.get(url, params=params, headers=headers, cookies=cookies)
        except Exception as err:
            message = err
            logger.add_log(__name__, message, logger.WARNING)
            raise ValueError(message)
        
        # Verify Response

        if response.status_code == 200:
            message = '200 OK - API query was successful'
            logger.add_log(__name__, message, logger.INFO)
            
            # Convert response to directory or json object
            obj_json = json.loads(response.text)

            return obj_json

        elif response.status_code >= 400:
            message = '400 Client Error'
            logger.add_log(__name__, message, logger.WARNING)
            raise ValueError(message)

        elif response.status_code >= 500:
            message = '500 Server Error'
            logger.add_log(__name__, message, logger.WARNING)
            raise ValueError(message)


    @staticmethod
    def crawler_connection(url, size_spider, **params):
        return ScrapperMiddleWare(url, size_spider, **params)
