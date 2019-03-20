import scrapy
import copy
import re, sys
from scrapy.selector import Selector


class GenericSpider(scrapy.Spider):
    name = "generic"

    def __init__(self, url, spider_size, tree_data):
        """ constructor 
            Receive:
            string: url for first extraction "www.example.com/" 
            tuple: spider_size (height, width)
            dictionary: html_structure must have contain the list of scrapy strings for every field
            list: structure_data_response is a output parameter of response extraction
            Description: asignation of values
            Return: None """        
        self.url = url
        self.spider_size = spider_size
        self.tree_data = tree_data
        self.global_links = [self.url]
        self.base_url = ""
        self.parents_level = "Seed"
    
    @property
    def global_links(self):
        try:
            global_links_local = self.__global_links
        except AttributeError:
            global_links_local = [] 
        return global_links_local

    @global_links.setter
    def global_links(self, links):
        try:
            self.__global_links.extend(links)
        except AttributeError:
            self.__global_links = []
            self.__global_links.extend(links)
    
    @property
    def children_list(self):
        try:
            children_list_local = self.__children_list
        except AttributeError:
            children_list_local = [] 
        return children_list_local
    
    @children_list.setter
    def children_list(self, links):
        try:
            self.__children_list.append(links)
        except AttributeError:
             self.__children_list = []
             self.__children_list.append(links)

    def start_requests(self):
        print(""" Create tree for her extraction""")
        level = 0
        index_current_node = 0
        max_level = self.spider_size[0]
        count_bad_request = 0
        index_children = 0
        links_current_node = []
        links_current_node.append(self.url)

        while level < max_level:
            #print(""" ... Extracting ... """, count_bad_request)
            count_bad_request += 1

            for current_link in links_current_node:
                    #print("current_link >==   ", current_link)
                    yield scrapy.Request(url=current_link, callback=self.parse)
                
            if index_children != len(self.children_list):
                links_current_node = self.children_list[index_current_node]
                index_children = len(self.children_list)
                index_current_node += 1
                count_bad_request = 0

            if self.next_level():
                level += 1

            if count_bad_request > 10000:
                print(""" 
                    10,000 Iteraciones
                        """)
                break
        self.tree_data[1] = self.global_links
        print("LEVEL MAX ", level)
        print("Cantidad de link sets", len(set(self.global_links)))
        print("Cantidad de link ", len(self.global_links))

    def parse(self, response):
        """ Extractor """
        children_current_node = self.extract_links(response)
        filtered_children_current_node = self.filter_links(children_current_node)

        self.global_links = filtered_children_current_node
        self.children_list = filtered_children_current_node
        self.tree_data[0][response.url] = filtered_children_current_node
       # self.log('URL: {} Finish'.format(response.url))

    def extract_links(self, response):
        links = response.xpath('//a[contains(@href,"https://www.yucatan.com.mx/")]').css('a::attr(href)').extract()
        links = list(set(links))
        return links

    def filter_links(self, links_current_node):
        clean_links_current_node = [link for link in links_current_node if links_current_node.count(link) == 1]
        clean_global_list = [link for link in clean_links_current_node if self.global_links.count(link) == 0]
        return clean_global_list[:self.spider_size[1]:]
 
    def next_level(self):
        current_children = []
        if self.parents_level == "Seed":
            if self.tree_data[0].get(self.url) is None:
                return False
            else:
                self.parents_level = [self.url]
                return False
        elif self.parents_level == []:
            return False
        else: 
            #print("                 ",self.parents_level)
            for link_parent in self.parents_level:
                children_temp = self.tree_data[0].get(link_parent)
                current_children.extend(children_temp)
                for link_children in children_temp:
                    if self.tree_data[0].get(link_children) is None:
                        return False
            self.parents_level = current_children
        return True
        