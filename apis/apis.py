import sys
sys.path.append('./../')
from general.connections import Connection, ConnectorAPI, Connector
from general.geomodel import GeoModel
from crawler.spider_middleware import SpiderMiddleWare
from general.Mapper import DefaultMapper
from test import Test
class GoogleAPI(ConnectorAPI):
    url = ''

    def __init__(self, abstract_mapper=None):
        super(GoogleAPI, self).__init__(self.url, abstract_mapper)

class YelpAPI(ConnectorAPI):
    url = ''

    def __init__(self, abstract_mapper=None):
        super(YelpAPI, self).__init__(self.url, abstract_mapper)

class InegiAPI(ConnectorAPI):
    url = 'https://www.inegi.org.mx/app/api/denue/v1/consulta/BuscarEntidad/restaurantes/31/1/50/fa649f90-1152-4121-94cf-b77bd199b9f0'

    MAP_COMMON_DATA = {
        'longitud': 'Longitud',
        'latitud': 'Latitud',
        'data': 'Clase_actividad'
    }

    METADATA = {
        'Estrato': '',
        'tipo_corredor_industrial': '',
        'nom_corredor_industrial': '',
        'Correo_e': '',
        'Sitio_internet': ''
    }

    def __init__(self, abstract_mapper=None):
        super(InegiAPI, self).__init__(self.url, abstract_mapper)

    def set_filter(self, places, state, firts, end):
        pass


class GenericAPI(ConnectorAPI):

    def __init__(self, url, abstract_mapper=None):
        super(GenericAPI, self).__init__(self.url, abstract_mapper)

    def consult(self):
        print('Consult method')

    def store(self):
        print('Store method')

    def map_out(self):
        print('Map out method')


class Crawler(Connector):


    def set_params(self, url, size_spider, **kwords):
        self.url = url
        self.size_spider = size_spider
        self.params = kwords
        self.crawler = SpiderMiddleWare(self.url, self.size_spider, **self.params)


    def consult(self):
        self.__data_structure__ = self.crawler.run_spider()

        Test(self.__data_structure__[1][0], self.url).run()

        return self.__data_structure__[0]
    
    

    def map_out(self):
        return DefaultMapper.mapout_crawler(self.__data_structure__[0])
    
