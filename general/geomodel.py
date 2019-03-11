from _datetime import datetime


class GeoModel(object):

    def __init__(self, data, metadata, latitude=0.0, longitude=0.0):
        self.latitude = latitude
        self.longitude = longitude
        self.date = '{0}'.format(datetime.now())
        self.data = data
        self.metadata = metadata.copy()

    def __str__(self):
        return ('Data: {} Metadata:{} \n'.format(self.data, self.metadata))


