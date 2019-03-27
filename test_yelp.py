# First you must import the following
from extractor import ConnectorFactory
from general.yelp_mapper import YelpMapper

# In this case, a custom dispatcher has been created, since DefaultMapper 
# would not work, so you get an instance of the custom mapper class 
mapper = YelpMapper()

# Now get the instance of the class from which we are going to obtain data 
# And we passed the custom mapper class
obj_yelp = ConnectorFactory.get_connector(ConnectorFactory.YELP_API, mapper)

# If we do not pass any parameters, it returns the following error:
#     get_connector() missing 1 required positional argument: 'source'

# if only the type of instance that we want to obtain happens to you, it will 
#     not mark an error when you execute the .consult () method, since you will
#     not be able to create the list

# If we only pass as a parameter the class of the custom dispatcher, after you try to execute any method, 
#     it will return an error like the following:
#     'NoneType' object has no attribute 'set_filter'

# Now we execute the set_filter method
obj_yelp.set_filter('delis','37.786882','-122.399972')

# If that method is not executed, then it returns the following error:
#     You need execute .set_filter() method before .consult().

# Now we execute the set_auth method
obj_yelp.set_auth()

# If that method is not executed, then it returns the following HTTP error:
#     400 Client Error

# Finally, if all goes well, the .consult () method is applied and the list of data is obtained
listmodels = obj_yelp.consult()

print(listmodels)