import sys
sys.path.append('./../')
from general.connections import Connection, ConnectorAPI, Connector
from general.geomodel import GeoModel
from crawler.spider_middleware import SpiderMiddleWare
from general.Mapper import DefaultMapper
from test import Test
from crawler.tree import Tree
import copy

# SUMMARY: Connector class to Google Maps API

class GoogleAPI(ConnectorAPI):

    # SUMMARY: Url is a property that overwrites the one it is inheriting.
    url = ''

    # SUMMARY: Initializer or constructor of the class
    def __init__(self, abstract_mapper=None):
        super(GoogleAPI, self).__init__(self.url, abstract_mapper)

# SUMMARY: Connector class to Yelp API
class YelpAPI(ConnectorAPI):

    # SUMMARY: Url is a property that overwrites the one it is inheriting.
    url = ''

    # SUMMARY: Initializer or constructor of the class
    def __init__(self, abstract_mapper=None):
        super(YelpAPI, self).__init__(self.url, abstract_mapper)

# SUMMARY: Connector class to DENUE API by INEGI
class InegiAPI(ConnectorAPI):
    
    # SUMMARY: Url is a property that overwrites the one it is inheriting.
    url = ''

    # SUMMARY: token is a property to InegiAPI class
    token = 'fa649f90-1152-4121-94cf-b77bd199b9f0'

    # SUMMARY: MAP_COMMON_DATA is a dictionary that overwrites the one it is inheriting.
    #     Its function is to establish the name of the properties 
    #     from which it will extract the common information for the model
    MAP_COMMON_DATA = {
        'longitud' : 'Longitud',
        'latitud' : 'Latitud',
        'data' : 'Clase_actividad'
    } 

    # SUMMARY: METADA is a dictionary that overwrites the one it is inheriting.
    #     Its function is to establish the name of the properties to determine
    #     the information with a high degree of value and add it to the model
    METADATA = {
        'Estrato' : '',
        'tipo_corredor_industrial' : '',
        'nom_corredor_industrial' : '',
        'Correo_e' : '', 
        'Sitio_internet' : '' 
    }

    # SUMMARY: Initializer or constructor of the class
    def __init__(self, abstract_mapper = None):
        super(InegiAPI, self).__init__(self.url, abstract_mapper)

    # SUMMARY: Method that establishes the url according to filter parameters
    # PARAM place: It is a string type parameter, which establishes the 
    #     category of places to be obtained, in the Places class, there are checked categories
    # PARAM state: It is a parameter of type string, which establishes the 
    #     state code, it can be obtained from the constants of the MexicoStates class
    # PARAM firts: Start number for the range of data to be extracted
    # PARAM end: End number for the range of data to be extracted
    def set_filter(self, place, state, firts, end):

        self.url = 'https://www.inegi.org.mx/app/api/denue/v1/consulta/BuscarEntidad/{0}/{1}/{2}/{3}/{4}'.format(place, state, firts, end, self.token)


# SUMMARY: Connector class to any API 
class GenericAPI(ConnectorAPI):

    # SUMMARY: Url is a property that overwrites the one it is inheriting.
    def __init__(self, url, abstract_mapper=None):
        super(GenericAPI, self).__init__(self.url, abstract_mapper)

    # SUMMARY: Unproven functionality
    def consult(self):
        print('Consult method')

    # SUMMARY: Unproven functionality
    def map_out(self):
        print('Map out method')


class Crawler(Connector):
    """ This is class use the user """


    def set_params(self, url, size_spider, **kwords): 
        """ Receive:
            string: url for first extraction "www.example.com/" 
            tuple: spider_size (height, width)
            **kowrds: key-value example title={dict with format crawler extraction}
            Description: asignation of values
            Return: None """   
        self.url = url
        self.size_spider = size_spider
        self.params = kwords
        self.crawler = Connection.crawler_connection(self.url, self.size_spider, **self.params)


    def consult(self):
        """ Receive:None
            Description: get data of spider
            Return: list of the dict, each dict is one item(note) """  
        self.__data_structure__ = self.crawler.run_spider()        
        return self.__data_structure__[0]

    def map_out(self):
        """ Receive:None
            Description: maps dictionary data in objects GeoModel
            Return: list of the objects GeoModel"""  
        return DefaultMapper.mapout_crawler(copy.copy(self.__data_structure__[0]))

    
    def get_tree(self):
        """ Receive:None
            Description: return the tree and list of the links
                list[0]  == tree, list[1] == list of the links 
            Return: list of the size two""" 
        tree = Tree(self.__data_structure__[1], self.__data_structure__[2], self.map_out())

        return tree, self.__data_structure__[2]

    def filter_data(self, text):
        """ Receive:
            string: text is the string
            Description: find into the data for each item in the tree
            return: list of the dict key is the url and value is one object the geomodel""" 
        filter_dict = []
        text_upper = text.upper()
        
        for item in self.__data_structure__[0]:
            if(not item["data"].upper().find(text_upper) == -1):
                filter_dict.append(copy.copy(item))
        return DefaultMapper.mapout_crawler(filter_dict)