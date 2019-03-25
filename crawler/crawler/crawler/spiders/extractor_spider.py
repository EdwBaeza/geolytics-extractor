import scrapy
import copy
import re, sys
from scrapy.selector import Selector
sys.path.append('./../../../../')
from general.log import logger


class ExtractorSpider(scrapy.Spider):
    name = "extractor"

    def __init__(self, urls, html_structure, structure_data_response):
        """ constructor 
            Receive:
            string: urls found in the generic_spider 
            dictionary: html_structure must have contain the list of scrapy strings for each field
            list: structure_data_response is a output parameter of response extraction
            Description: asignation of values
            Return: None """        
        self.urls = urls
        self.html_structure = html_structure
        self.structure_data_response = structure_data_response
        self.metadata = copy.copy(self.html_structure)
        del (self.metadata["title"])
        del (self.metadata["data"])

    def start_requests(self):
        """ *Receive:
            *Description: request for each url found in the generic_spider
            *Return: None"""
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """ *Receive:
            Response: response is the reponse of request for each url (html for example)" 
            *Description: call to extract_text function sending the structure each field
            *Return: None """     
        
        title = self.extract_text(response, self.html_structure["title"])
        data = self.extract_text(response, self.html_structure["data"])
        dict_metadata = dict()
        
        if title == '' or data == '':
            logger.add_log(__name__, "DATA NOT FOUND IN URL: {}".format(response.url), logger.INFO)
            return
        print("----- METADATA-----")
        print(self.metadata)
        for item_metadata in self.metadata.keys():
            item_metadata_content = self.extract_text(response, self.metadata[item_metadata])
            dict_metadata[item_metadata] = item_metadata_content

        page = dict(title=title, data=data, metadata=dict_metadata, url=response.url)
        self.structure_data_response.append(page)

    def extract_text(self, response, scrapy_strings):
        """ *Receive
            Response: response is the reponse of request for each url (html for example)"
            scrapy_strings: 
            *Description: extract text pure of html (use scrapy selectors)
                clean space (use regex)
                clean \n    (use regex)
                clean html  (use regex)
                clean scripts (use regex)
            *Return: None """     
        data = ['']
        if len(scrapy_strings) == 1:
            data = response.xpath(scrapy_strings[0]).extract()
        elif len(scrapy_strings) == 2:
            data = response.css(scrapy_strings[0]).xpath(scrapy_strings[1]).extract()
        elif len(scrapy_strings) == 3:
            predata = response.css(scrapy_strings[0]).xpath(scrapy_strings[1]).get()
            data[0] = predata
            #data = Selector(text=predata).xpath(scrapy_strings[2]).extract()
        else:
            print(scrapy_strings, ' <- ss    len->', len(scrapy_strings))
            logger.add_log(__name__, "Error in size scrapy_strings", logger.CRITICAL)
            raise ValueError("Error in size scrapy_strings")

        if not data or (data and data[0] is None):
            return ''

        regex_string_html = r"<.*?>"
        regex_string_space = r"\s+"
        regex_string_linebreak = r"\n+"
        regex_string_script = r"<script(\s?.\s?)*?>(\s?|.)*?(<\/script>)"

        regex_html = re.compile(regex_string_html)
        regex_space = re.compile(regex_string_space)
        regex_linebreak = re.compile(regex_string_linebreak)
        regex_scripts = re.compile(regex_string_script)

        data_without_scripts = regex_scripts.sub("", data[0])
        data_without_html = regex_html.sub("", data_without_scripts)
        data_without_linebreak = regex_linebreak.sub("\n", data_without_html)
        data_without_spaces = regex_space.sub(" ", data_without_linebreak)

        return data_without_spaces
