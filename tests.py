
from extractor import ConnectorFactory
from apis.filters import Places, MexicoStates

obj_inegi = ConnectorFactory.get_connector(ConnectorFactory.INEGI_API)

obj_inegi.set_filter(Places.RESTAURANTES,MexicoStates.YUCATAN,1,10)

print(obj_inegi.url)

listmodels = obj_inegi.consult()

print(listmodels)