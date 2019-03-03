from abc import ABCMeta, abstractmethod
import requests 
import json
from log import logger
from Mapper import AbstractMapper, DefaultMapper
from UnstructedDB.scrapper import Scrapper
  
# Abstract class
class Connector(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def consult(self):
        print('Consult method')

    @abstractmethod
    def store(self):
        print('Store method')

    @abstractmethod
    def map_out(self):
        print('Map out method')


class ConnectorAPI(Connector):

    MAP_COMMON_DATA = {}

    COMMON_DATA = {
        'longitud' : '',
        'latitud' : '',
        'data' : ''
    }

    METADATA = {}

    mapper = AbstractMapper()

    def __init__(self, url, abstract_mapper = None):
        self.url = url
        if abstract_mapper is None:
            self.mapper = DefaultMapper()
        else:
            self.mapper = abstract_mapper

    def consult(self):
        try:
            self.obj_json = Connection.api_connection(self.url)
            self.map_out()
            #listModel = self.map_out()
            #return listModel
        except Exception as err:
            print(err)

    def store(self):
        print('Store method')

    def map_out(self):
        self.mapper.mapout_API(self.obj_json, self.MAP_COMMON_DATA, self.METADATA)


# Class with diferent kind methods connection

class Connection(object):

    # De este modo ya se puede hacer consultas con parámetros, cabeceras y cookies.
    # Falta que pueda hacer consultas con Autentificación OAuth1.0 y OAuth2.0.
    # Al igual que autentificaciones básicas.
    # Tener encuenta que no hay forma de pasar Path Variable, ya se debe definir
    # en le url.    
    @staticmethod
    def api_connection(url, params=None, headers=None, cookies=None):

        message = ''
        response = ''

        try:
            response = requests.get(url, params=params, headers=headers, cookies=cookies)
        except Exception as err:
            message = err
            logger.add_log(__name__, message, logger.WARNING)
            raise ValueError(message)
        

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
        return Scrapper(url, size_spider, **params)
