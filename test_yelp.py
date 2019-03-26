from extractor import ConnectorFactory
from general.yelp_mapper import YelpMapper




mapper = YelpMapper()

obj_yelp = ConnectorFactory.get_connector(ConnectorFactory.YELP_API, mapper)




obj_yelp.set_filter('delis','37.786882','-122.399972')

obj_yelp.set_auth()



listmodels = obj_yelp.consult()

print(listmodels)