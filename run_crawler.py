""" geolytics extractor"""
from extractor import ConnectorFactory

def run():

    
    url = "https://www.yucatan.com.mx/"
    size_spider = (10, 10)
    #format crawler extraction
    attr_data = {"class": "entry-content", "itemprop": "articleBody"}
    attr_title = {"class": "g1-mega", "itemprop": "headline"}
    attr_date = {"class": "entry-date", "itemprop": "datePublished"}
    attr_category = {"itemprop": "articleSection"}
    """<h1 class="g1-mega g1-mega-1st entry-title" itemprop="headline"></h1>"""
    title = {"tag":"h1", "attr": attr_title}
    """"<div class="entry-content g1-typography-xl" itemprop="articleBody"></div>"""
    data = {"tag":"div", "attr": attr_data}

    """<time class="entry-date" datetime="2019-02-08T00:06:36" itemprop="datePublished"><time> 
    <a href="https://www.yucatan.com.mx/seccion/deportes" class="entry-category entry-category-item-4">
        <span itemprop="articleSection">Deportes</span>
    </a>
    Example ID Data or Title example = {"tag": "div", "id": "secondary"}
    Example ID Metadata example = { "name": "advertising", "tag": "div", "id": "secondary"} 
     """
    metadata = ({"name": "post_date", "tag": "time", "attr": attr_date},
              {"name": "category", "tag": "span", "tag_parent" : "a", "attr": attr_category})
    crawler = ConnectorFactory.get_connector(ConnectorFactory.CRAWLER)
    crawler.set_params(url, size_spider, title=title, data=data, metadata=metadata)
    data = crawler.consult()
    data_tree = crawler.map_out()
    node_list = crawler.filter_data("una")
    tree = crawler.get_tree()

    print("COUNT DATA EXTRACTED", len(data), "/", len(tree[1]))
    print("COUNT NODE LIST EXTRACTED (Mapper)", len(node_list))
    for item in data:
        print(item)
        inp = input("ENTER TO NEXT")
        if inp == 'q':
            break

    # data = tree[0].Get_data()
    # print(data)
    # children = tree[0].Get_Front_Position()
    # print(children)

run()
