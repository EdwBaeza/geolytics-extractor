from abc import ABCMeta, abstractmethod
from .geomodel import GeoModel
import json

class AbstractMapper(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def mapout_API(self,data_not_mapped):
        pass
    
    @abstractmethod
    def  mapout_DB_Unstructed(self,data_not_mapped):
        pass


class DefaultMapper(AbstractMapper):
    
    def mapout_API(self, obj_json, common_data, metadata):
        
        copy_metadata = {}
        objs_list = []

        for data_obj in obj_json:

            copy_metadata = metadata.copy()
            
            longitude = data_obj[common_data['longitud']]

            latitude = data_obj[common_data['latitud']]

            data = data_obj[common_data['data']]

            for key in metadata.keys():
                if data_obj[key] != '':
                    copy_metadata[key] = data_obj[key]
                else:
                    del copy_metadata[key]

            #creamos un objeto GeoModel
            model = GeoModel(data,copy_metadata,latitude,longitude)

            # __dict__ -> Convierte el objeto a diccionario
            # y se agrega a la lista de objectos GeoModel
            objs_list.append(model.__dict__)

            copy_metadata.clear()

        #Retornamos la lista de objetos GeoModel en formato Json
        return json.dumps(objs_list, indent=4)

    def  mapout_DB_Unstructed(self, data_not_mapped):
        pass