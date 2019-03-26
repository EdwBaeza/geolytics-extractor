from unittest import TestCase
from extractor import ConnectorFactory
from general.geomodel import GeoModel
from crawler.tree import Tree
class CrawlerTest(TestCase):
    """ Crawler debe contener los siguientes métodos:
        Método Consultar
        Método Map out
        Método SetParams
        Método Get Tree
        Método Filter Data
        """

    def set_up(self):
        """ Metodo Inicial """
        #Sólo se obtendrán datos de un mismo dominio, el cual se considerará origen.
        url = "https://www.yucatan.com.mx/"
        #Se Podra definir el tamaño del árbol mediante su profundidad y número de hijos máxima por nodo
        size_spider = (3,2) # (Produndidad, NumeroMaximoDeHijosPorNodo)
        attr_data = {"class": "entry-content", "itemprop": "articleBody"}
        attr_title = {"class": "g1-mega", "itemprop": "headline"}
        attr_date = {"class": "entry-date", "itemprop": "datePublished"}
        attr_category = {"itemprop": "articleSection"}
        #Existirán constantes que describirán los features que ya son conocidos para el origen de datos(title y data)
        #página noticias existirá un metadata que contendrá un feature de tipo título.
        title = {"tag":"h1", "attr": attr_title}
        data = {"tag":"div", "attr": attr_data}
        #Existirán Features definidos por el usuario. (Dentro de metadata)
        metadata = ({"name": "post_date", "tag": "time", "attr": attr_date},
                  {"name": "category", "tag": "span", "tag_parent" : "a", "attr": attr_category})
        #Para generar la instancia debe utilizar el patrón de diseño factory.
        self.crawler = ConnectorFactory.get_connector(ConnectorFactory.CRAWLER)
        #Método SetParams
        self.crawler.set_params(url, size_spider, title=title, data=data, metadata=metadata)
    
    def test_consult(self):
        #Método Consultar
        data = self.crawler.consult()
        print(len(data))
        self.assertIsInstance(data, list, "Debe ser una lista")
        for item in data:
            data = item.get('data')
            metadata = item.get('metadata')
            #Cada features será una tupla llave valor
            #Existirán constantes que describirán los features que ya son conocidos para el origen de datos página(title y metadata) noticias existirá un metadata que contendrá un feature de tipo título.
            self.assertIsInstance(item, dict, "Debe ser un diccionario cada item de la lista de datos")
            self.assertIsNotNone(data, "Debe Contener El Campo data")
            self.assertIsNotNone(metadata, "Debe Contener El Campo metadata(Puede Estar vacio pero debe estar)")
            self.assertIsNotNone(metadata.get('title'), "Debe Contener El Campo title")

    def test_map_out(self):
        #La estructura de los datos obtenidos, deberá ser la siguiente: [ data, fecha de obtención,metadata ](este caso es una diccionario donde la llave sera cara url encontrada(que tenga minimamente title y data)y su valor sera un objeto GeoModel con los atributos mencionados anteriormente)
        #Ejemplo {'https://www.milenio.com//policia/en-24-horas-caen-en-la-cdmx-seis-colombianos-mas': <general.geomodel.GeoModel object at 0x10fbd0a90>}
        data = self.crawler.map_out()
        self.assertIsInstance(data, dict, "Debe una instancia de dict")
        for item in data.values():
            self.assertIsInstance(item, GeoModel, "Debe Ser Una instancia de GeoModel")

    def test_filter_data(self):
        #Se deberán poder extraer los datos con los siguientes filtros: Por data
        data = self.crawler.filter_data("Pymes")
        self.assertIsInstance(data, dict, "Debe una instancia de dict")
        for item in data.values():
            self.assertIsInstance(item, GeoModel, "Debe Ser Una instancia de GeoModel")

        
    def test_get_tree(self):
        data = self.crawler.filter_data("Pymes")
        self.assertIsInstance(data, dict, "Debe Contener El Campo data")

test = CrawlerTest()
test.set_up()
test.test_consult()
test.test_map_out()
test.test_filter_data()
test.test_get_tree()

