""" geolytics extractor"""
from extractor import ConnectorFactory

def run():
    url = "https://www.yucatan.com.mx/"
    size_spider = (10, 10)
    attr_data = {"class": "entry-content","itemprop": "articleBody"}
    attr_title = {"class": "g1-mega","itemprop": "headline"}
    attr_date = {"class": "entry-date","itemprop": "datePublished"}
    attr_category = {"itemprop": "articleSection"}
    """<h1 class="g1-mega g1-mega-1st entry-title" itemprop="headline"></h1>"""
    title = {"tag":"h1", "attr": attr_title}
    """"<div class="entry-content g1-typography-xl" itemprop="articleBody"></div>"""
    data = {"tag":"div", "attr": attr_data}
    """<time class="entry-date" datetime="2019-02-08T00:06:36" itemprop="datePublished"><time> """
    """<a href="https://www.yucatan.com.mx/seccion/deportes" class="entry-category entry-category-item-4">
        <span itemprop="articleSection">Deportes</span>
        </a>"""
    """Example ID { "name": "advertising", "tag": "div", "id": "secondary"} """
    metadata = ({"name": "post_date", "tag": "time", "attr": attr_date},
              {"name": "category", "tag": "span", "tag_parent" : "a", "attr": attr_category})
    crawler = ConnectorFactory.get_connector(ConnectorFactory.CRAWLER)
    crawler.set_params(url, size_spider, title=title, data=data, metadata=metadata)
    data = crawler.consult()
    node_list = crawler.map_out()
    print("COUNT DATA EXTRACTED", len(data))
    print("COUNT NODE LIST EXTRACTED", len(node_list))
    for item in node_list:
        print(item)
        inp = input("ENTER TO NEXT")
        if inp == 'q':
            break

run()
