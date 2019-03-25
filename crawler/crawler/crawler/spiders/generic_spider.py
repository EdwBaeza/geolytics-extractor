import scrapy
import copy
import re, sys
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider

class GenericSpider(scrapy.Spider):
    name = "generic"

    def __init__(self, url, spider_size, tree_data):
        """ constructor 
            Receive:
            string: url for first extraction "www.example.com/" 
            tuple: spider_size (height, width)
            list: tree_data is a output parameter for response the tree(dict) and list of the links of tree. tree_data[0] is tree and tree_data[1] is list of the links
            Description: asignation of values
            Return: None """        
        self.url = url
        self.spider_size = spider_size
        self.tree_data = tree_data
        self.global_links = [self.url]
        self.parents_level = "Seed"
        self.level = 0
        self.max_links = self.get_max_links()
    
    @property
    def global_links(self):
        """ property global_links (get)"""
        try:
            global_links_local = self.__global_links
        except AttributeError:
            global_links_local = [] 
        return global_links_local

    @global_links.setter
    def global_links(self, links):
        """ property global_links (set) union the list"""
        try:
            self.__global_links.extend(links)
        except AttributeError:
            self.__global_links = []
            self.__global_links.extend(links)
    
    @property
    def children_list(self):
        """ property chilndren list (get) """
        try:
            children_list_local = self.__children_list
        except AttributeError:
            children_list_local = [] 
        return children_list_local
    
    @children_list.setter
    def children_list(self, links):
        """ property chilndren list (set) add the last """
        try:
            self.__children_list.append(links)
        except AttributeError:
             self.__children_list = []
             self.__children_list.append(links)

    def start_requests(self):
        """ *Receive:
            *Description: request for each url found in extraction bucle
            bucle until max_level(height)
            *Return: None"""

        index_current_node = 0
        max_level = self.spider_size[0]
        count_bad_request = 0
        index_children = 0
        links_current_node = []
        links_current_node.append(self.url)

        while self.level < max_level:

            print(""" 
            
            links
            """)

            print(links_current_node)
            print(""" 
            
            
            """)
            count_bad_request += 1
            for current_link in links_current_node:
                    yield scrapy.Request(url=current_link, callback=self.parse)

            if self.next_level():
                self.level += 1

            if index_children != len(self.children_list) and self.level < max_level:
                links_current_node = self.children_list[index_current_node]
                index_children = len(self.children_list)
                index_current_node += 1
                count_bad_request = 0

            if count_bad_request > 10000:
                print(""" 
                    10,000 Iteraciones
                        """)
                break
        self.tree_data[1] = self.global_links[:self.max_links:]

    def parse(self, response):
        """ *Receive:
            Response: response is the reponse of request for each url (html for example)" 
            *Description: 
            call to extract_links function sending the response for get links of this node.
            *Return: None """     
        len_global_links = len(self.global_links)
        if self.max_links > len_global_links :
    
            children_current_node = self.extract_links(response)
            filtered_children_current_node = self.filter_links(children_current_node)
            self.global_links = filtered_children_current_node
            self.children_list = filtered_children_current_node
            self.tree_data[0][response.url] = filtered_children_current_node



    def extract_links(self, response):
        """ *Receive:
            Response: response is the reponse of request for each url (html for example)" 
            *Description: extract links of html (use scrapy selectors)
            *Return: list of links no repeated """
        links_without_protocol = response.css('a::attr(href)').re("^(\/.+)$")
        links_with_protocol = response.xpath('//a[contains(@href,"{}")]'.format(self.url)).css('a::attr(href)').extract()
        links = ["{}{}".format(self.url, link) for link in links_without_protocol]
        links.extend(links_with_protocol)
        links = list(set(links))
        return links

    def filter_links(self, links_current_node):
        """ *Receive:
            list: links_current_node is a list of links, this list represent children of current node
            *Description: delete repeated links (use list comprehension and slicing)
            *Return: list  of links no repeated """
        clean_links_current_node = [link for link in links_current_node if links_current_node.count(link) == 1 and not link == '']
        clean_global_list = [link for link in clean_links_current_node if self.global_links.count(link) == 0 and not link == '']

        max_spider =  clean_global_list[:self.spider_size[1]:]
        # protocol_none =  [link for link in links_current_node if link.count(self.url[0])== -1 and not link == '']
        # protocol_ok = [link for link in links_current_node if not link in protocol_none]
        # protocol_none_to_ok = ["{}{}".format(self.url[0],link) for link in links_current_node if not link == '']
       
        return max_spider
 
    def next_level(self):
        """ *Receive:None
            *Description: validates if a level was advanced in the tree,
            taking the children from a previous level who are now parents of the current nodes
            *Return: Bool True advanced or False not advanced"""
        current_children = []
        if self.parents_level == "Seed":
            if self.tree_data[0].get(self.url) is None:
                return False
            else:
                self.parents_level = [self.url]
                return True
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
        
    def get_max_links(self):
        """ *Receive: None
            *Description: calculates the maximum number of children the tree can have based on its width and height
            *Return: int number of the max children in the tree """
        mul = 1
        ac = 1
        for i in range(self.spider_size[0]):
            pow = i + 1
            mul = self.spider_size[1] ** pow
            ac+= mul
        return ac
    