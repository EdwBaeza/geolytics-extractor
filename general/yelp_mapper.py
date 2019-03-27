from .Mapper import AbstractMapper
from .geomodel import GeoModel
import json

class YelpMapper(AbstractMapper):

    def mapout_API(self, obj_json, common_data, metadata):

        copy_metadata = {}
        objs_list = []

        for data_obj in obj_json['businesses']:

            copy_metadata = metadata.copy()
            
            # Extract common data
            longitude = data_obj['coordinates'][common_data['longitud']]
            latitude = data_obj['coordinates'][common_data['latitud']]
            data = data_obj[common_data['data']]

            # Extract metadata
            for key in metadata.keys():
                if data_obj[key] != '':
                    copy_metadata[key] = data_obj[key]
                else:
                    del copy_metadata[key]

            # A GeoModel object is created
            model = GeoModel(data,copy_metadata,latitude,longitude)

            # __dict__ -> Convert the object to a dictionary
            # and it is added to the GeoModel object list
            objs_list.append(model.__dict__)

            copy_metadata.clear()

        # return a list of geomodel class in json format
        return json.dumps(objs_list, indent=4)
    

    def mapout_DB_Unstructed(self):
        pass