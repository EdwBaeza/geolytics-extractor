import scrapy
import copy
import re, sys
from scrapy.selector import Selector


class GenericSpider(scrapy.Spider):
    name = "generic"

    def __init__(self, url, spider_size, html_structure, structure_data_response, exist_metadata):
        """ constructor 
            Receive:
            string: url for first extraction "www.example.com/" 
            tuple: spider_size (height, width)
            dictionary: html_structure must have contain the list of scrapy strings for every field
            list: structure_data_response is a output parameter

            Description: asignation of values
            Return: None
        """        
        self.url = url
        self.spider_size = spider_size
        self.html_structure = html_structure
        self.structure_data_response = structure_data_response
        self.exist_metadata = exist_metadata
        self.metadata = copy.copy(self.html_structure)
        self.global_links = []
        self.children_list = []
        self.base_url = ""
        del (self.metadata["title"])
        del (self.metadata["data"])

    def start_requests(self):
        print( """ Create tree for her extraction""")
        level = 0
        index_currente_node= 0
        max_level = self.spider_size[0]
        max_children = self.spider_size[1]

        count_bad_request = 0
        count_width = 0
        index_children = 0
        links_current_node = []
        links_current_node.append(self.url)

        while level <= max_level:
            print(""" ... Extracting ... """, count_bad_request)
            count_bad_request += 1
            for current_link in links_current_node:
                count_width +=1
                yield scrapy.Request(url=current_link, callback=self.parse)
                if count_width == max_children:
                    break
            if index_children != len(self.children_list):
                links_current_node = self.children_list[index_currente_node]
                index_children = len(self.children_list)
                index_currente_node += 1
                level += 1
                count_bad_request = 0

            if count_bad_request >5000:
                print(""" 
                
                
                    5,000 Iteraciones
                
                
                """)
                break
        print("LEVEL MAX ", level)

    @property
    def global_links(self):
        return self.__global_links

    @global_links.setter
    def global_links(self, links):
        try:
            self.__global_links.extend(links)
        except Exception:
            self.__global_links = []
            self.__global_links.extend(links)

    def parse(self, response):
        """ Extractor """

        children_current_node = self.extract_links(response)
        filtered_children_current_node = self.filter_links(children_current_node)

        self.global_links = filtered_children_current_node
        self.children_list.append(filtered_children_current_node)

        title = self.extract_text(response, self.html_structure["title"])
        data = self.extract_text(response, self.html_structure["data"])
        metadata_local = []
        dict_metadata = dict()
        if title == '' or data == '':
            return

        for item_metadata in self.metadata.keys():

            item_metadata_content = self.extract_text(response, self.metadata[item_metadata])
            dict_metadata[item_metadata] = item_metadata_content

        page = dict(title=title, data=data, metadata=dict_metadata)
        self.structure_data_response.append(page)

        self.log('URL: {} Finish'.format(response.url))

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
            print(response.url)
            print(scrapy_strings)
            print("DATA NOT FOUND")
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


    def extract_links(self, response):
        links = response.xpath('//a[contains(@href,"https://www.yucatan.com.mx/")]').css('a::attr(href)').extract()
        links = list(set(links))
        return links

    def filter_links(self, links_current_node):
        return [link for link in links_current_node if self.global_links.count(link) == 0]


