# First you must import the following
from extractor import ConnectorFactory
from apis.filters import Places, MexicoStates

# Now get the instance of the class from which we are going to obtain data
obj_inegi = ConnectorFactory.get_connector(ConnectorFactory.INEGI_API)

#If no parameter is sent, it returns the following error:
#     get_connector() missing 1 required positional argument: 'source'


# Now we execute the set_filter method
obj_inegi.set_filter(Places.RESTAURANTES,MexicoStates.YUCATAN,1,10)

# If that method is not executed, then it returns the following error:
#     You need execute .set_filter() method before .consult().

# Finally, if all goes well, the .consult () method is applied and the list of data is obtained
listmodels = obj_inegi.consult()

print(listmodels)