import sys
from general.connections import Connection, ConnectorAPI, Connector
#from UnstructedDB.scrapper import Scrapper
sys.path.append('./../')
from general.geomodel import GeoModel

class GoogleAPI(ConnectorAPI):
    url = ''

    def __init__(self, abstract_mapper=None):
        super(GoogleAPI, self).__init__(self.url, abstract_mapper)

class YelpAPI(ConnectorAPI):
    url = ''

    def __init__(self, abstract_mapper=None):
        super(YelpAPI, self).__init__(self.url, abstract_mapper)

class InegiAPI(ConnectorAPI):
    
    url = ''
    token = 'fa649f90-1152-4121-94cf-b77bd199b9f0'

    MAP_COMMON_DATA = {
        'longitud' : 'Longitud',
        'latitud' : 'Latitud',
        'data' : 'Clase_actividad'
    } 

    METADATA = {
        'Estrato' : '',
        'tipo_corredor_industrial' : '',
        'nom_corredor_industrial' : '',
        'Correo_e' : '', 
        'Sitio_internet' : '' 
    }

    def __init__(self, abstract_mapper = None):
        super(InegiAPI, self).__init__(self.url, abstract_mapper)

    def set_filter(self, place, state, firts, end):

        self.url = 'https://www.inegi.org.mx/app/api/denue/v1/consulta/BuscarEntidad/{0}/{1}/{2}/{3}/{4}'.format(place, state, firts, end, self.token)



class GenericAPI(ConnectorAPI):

    def __init__(self, url, abstract_mapper=None):
        super(GenericAPI, self).__init__(self.url, abstract_mapper)

    def consult(self):
        print('Consult method')

    def store(self):
        print('Store method')

    def map_out(self):
        print('Map out method')

"""
class Crawler(Connector):


    def set_params(self, url, size_spider, **kwords):
        self.url = url
        self.size_spider = size_spider
        self.params = kwords
        self.crawler = Scrapper(self.url, self.size_spider, **self.params)


    def consult(self):
        self.__data_structure__ = self.crawler.run_spider()
        return self.__data_structure__

    def map_out(self):

        node_list = []

        for node  in self.__data_structure__:
            metadata = node.get('metadata')
            metadata['title'] = node.get('title')
            model = GeoModel(node.get('data'), metadata)
            node_list.append(model)

        return node_list


    def store(self):
        print("Metodo Implementado")
"""
