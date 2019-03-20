import scrapy
import copy
import re, sys
from scrapy.selector import Selector



class ExtractorSpider(scrapy.Spider):
    name = "extractor"

    def __init__(self, urls, html_structure, structure_data_response):
        """ constructor 
            Receive:
            string: url for first extraction "www.example.com/" 
            tuple: spider_size (height, width)
            dictionary: html_structure must have contain the list of scrapy strings for every field
            list: structure_data_response is a output parameter of response extraction
            Description: asignation of values
            Return: None """        
        self.urls = urls
        self.html_structure = html_structure
        self.structure_data_response = structure_data_response
        self.metadata = copy.copy(self.html_structure)
        del (self.metadata["title"])
        del (self.metadata["data"])
        print(""" 
        
        
        
            Constructor Extractor



        
        
        """)

    def start_requests(self):
        print("""



                AQUIIIIIIIIIII

            Links  generic spider extrctor
            {}
        
        



         """.format(len(self.urls)))
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """ Extractor """
        
        title = self.extract_text(response, self.html_structure["title"])
        data = self.extract_text(response, self.html_structure["data"])
        dict_metadata = dict()
        
        if title == '' or data == '':
            return

        for item_metadata in self.metadata.keys():
            item_metadata_content = self.extract_text(response, self.metadata[item_metadata])
            dict_metadata[item_metadata] = item_metadata_content

        page = dict(title=title, data=data, metadata=dict_metadata)
        self.structure_data_response.append(page)
       # self.log('URL: {} Finish'.format(response.url))

    def extract_text(self, response, scrapy_strings):
        """ extract pure text of html """
        if len(scrapy_strings) == 1:
            # content =  response.xpath('//div[contains(@id,"content-body")]').extract()
            data = response.xpath(scrapy_strings[0]).extract()
        elif len(scrapy_strings) == 2:
            # data = response.css("div.entry-content").xpath("//div[contains(@itemprop,'articleBody')]").extract()
            data = response.css(scrapy_strings[0]).xpath(scrapy_strings[1]).extract()
        elif len(scrapy_strings) == 3:
            """
            data = response.css("a span")
            .xpath("//span[contains(@itemprop,'articleSection')]").extract_first()
            data_ultimate = Selector(text=data).xpath("//span/text()").extract()
            """
            predata = response.css(scrapy_strings[0]).xpath(scrapy_strings[1]).extract_first()
            data = Selector(text=predata).xpath(scrapy_strings[2]).extract()
        else:
            print(scrapy_strings, ' <- ss    len->', len(scrapy_strings))
            raise ValueError("Error in size scrapy_strings")

        if len(data) == 0:
            print(""" DATA NOT FOUND """)
            return ""

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
