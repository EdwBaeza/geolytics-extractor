from abc import ABCMeta, abstractmethod
from .geomodel import GeoModel

class AbstractMapper(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def mapout_API(self,data_not_mapped):
        pass
    
    @abstractmethod
    def  mapout_crawler(self,data_not_mapped):
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

            print("")
            print("GEOMODEL:[point: Point({0},{1}), data: {2}, metadata: {3}]".format(longitude,latitude,data,copy_metadata))
            print("")

            #model = GeoModel(longitude, latitude, data, metadata)
            #model = GeoModel(data,metadata,latitude,longitude)

            #objs_list.append(model)

            copy_metadata.clear()
        
        #return json.dumps(objs_list)

    @staticmethod
    def  mapout_crawler(data_not_mapped):
        node_list = []
        for node  in data_not_mapped:
            metadata = node.get('metadata')
            metadata['title'] = node.get('title')
            model = GeoModel(node.get('data'), metadata)
            node_list.append(model)

        return node_list