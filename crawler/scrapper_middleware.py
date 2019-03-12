from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from .crawler.crawler.spiders.generic_spider import GenericSpider

class ScrapperMiddleWare(object):

    __FIND_BY_ID__ = 0
    __FIND_BY_ATTR__ = 1
    __FIND_BY_ATTR_PARENT__ = 3

    """ constructor 
        Receive:
        string: root_url for first extraction "www.example.com/" 
        tuple: spider_size (height, width)
        **kwords: params key-value, this field must contain the 
            title, data and metadata (metadata can have custom values)
            title and data are requiered  

        Description: asignation of values
        Return: None
    """
    def __init__(self, root_url, spider_size, **kwords):
        
        self.root_url = root_url
        self.spider_size = spider_size
        self.__html_structure__ = dict()
        self.__metadata_exist__ = False

        try:
            self.__data_validation__(kwords["title"], "title")
        except KeyError:
            raise ValueError("'title' not found")
        try:
            self.__data_validation__(kwords["data"], "data")
        except KeyError:
            raise ValueError("'data' not found")
        metadata = kwords.get("metadata")

        if metadata is not None:
            self.__metadata_exist__ = True
            self.__metadata_validation__(metadata)

    def __data_validation__(self, param, name):
        """ Receive
        dictionary: param must have tag and id or attr(it's dictionary)
        string: name, represent the name of param example title y data
        Description: verify the structure of every field 
        Return: None"""

        if param.get("tag") is None:
            raise ValueError("'{}' must have 'tag'".format(name))
        if param.get("id") is not None:
            param["findby"] = ScrapperMiddleWare.__FIND_BY_ID__
        elif param.get("attr") is None :
            raise ValueError("'{}' must have id or attr".format(name))
        elif len(param.get("attr")) is 1:
            param['findby'] = ScrapperMiddleWare.__FIND_BY_ATTR_PARENT__
        elif len(param.get("attr")) is 2:
            param['findby'] = ScrapperMiddleWare.__FIND_BY_ATTR__
        else:
            raise ValueError("'{}'in attr must contains 1 of 2 fields".format(name))
        self.__html_structure__[name] = self.__get_string_scrapy__(param)


    def __metadata_validation__(self, metadata):
        """ Receive
        dictionary: meatadata is a dictionary of dictionaries
        Description: verify the structure of every field into of metada.
        Return: None"""

        if type(metadata) == tuple:
            for item_metadata in metadata:
                if item_metadata.get("name") is None:
                    raise ValueError("The fields in metadata must have 'name'")
                else:
                    self.__data_validation__(item_metadata,item_metadata["name"])
        elif type(metadata) == dict:
            if metadata.get("name") is None:
                raise ValueError("The fields in metadata must have 'name'")
            else:
                self.__data_validation__(metadata, metadata["name"])


        """ Receive
        dictionary: param is a dictionary
        Description: convert the param to string of xpath or css(scrapy 
        library use the string css or xpath for extraction) for extraction. 
        Return: Scrapy String (css or xpath)"""
    def __get_string_scrapy__(self, param):
        # data =  response.xpath('//div[contains(@id,"content-body")]').extract()
        # data = response.css("div.entry-content").xpath("//div[contains(@itemprop,'articleBody')]").extract()
        if param["findby"] == ScrapperMiddleWare.__FIND_BY_ID__:
            string_scrapy = '//{}[contains(@id,"{}")]'.format(param["tag"], param["id"])
            return (string_scrapy,)

        elif param["findby"] == ScrapperMiddleWare.__FIND_BY_ATTR__:
            attr = param["attr"]
            attr_keys = list(attr.keys())
            attr_keys.remove("class")

            string_scrapy_class = "{}.{}".format(param["tag"], attr["class"])
            string_scrapy_other_attr = '//{}[contains(@{},"{}")]'.format(
                param["tag"],
                attr_keys[0],
                attr[attr_keys[0]])

            return (string_scrapy_class, string_scrapy_other_attr)
        elif param["findby"] == ScrapperMiddleWare.__FIND_BY_ATTR_PARENT__:
            attr = param["attr"]
            attr_keys = list(attr.keys())
            string_scrapy_first = '{} {}'.format(param['tag'], param['tag_parent'])
            string_scrapy_second = "//{}[contains(@{},'{}')]".format(
                param['tag'],
                attr_keys[0],
                attr[attr_keys[0]])
            string_scrapy_third = '//{}/text()'.format(param['tag'])
            return (
                string_scrapy_first,
                string_scrapy_second,
                string_scrapy_third)


    def run_spider(self):
        """ Receive: None
        Description: script for run spider independently of scrapy shell. 
        Return: """

        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        runner = CrawlerRunner()
        structure_data_return = []
        d = runner.crawl(GenericSpider, self.root_url, self.spider_size, self.__html_structure__,
                          structure_data_return, self.__metadata_exist__)
        d.addBoth(lambda _: reactor.stop())
        print("Run spider (scrapperMiddleWare)")

        try:
            reactor.run()
        except Exception as excep:
            print("ERROR -> ", excep)
            
        return structure_data_return
