class Test():

    def __init__(self, diccionario, url):
        test_dictionary = {'seed':['link1','link2','link3','link4'], 'link1':['link5','link6'], 'link2':['link7','link8','link9'], 
    'link3':['link10'], 'link4':['link11'], 'link5':[], 'link6':[], 'link7':[], 'link8':[], 'link9':[], 'link10':['link12'], 
    'link11':[], 'link12':[]}
        self.tree_data = [diccionario]
        self.parents_level = "Seed"
        self.url = url
        print(""" 
                cantidad de llaves
                {}
                """.format(len(diccionario.keys())))

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
            print(self.parents_level)
            for link_parent in self.parents_level:
                children_temp = self.tree_data[0].get(link_parent)
                current_children.extend(children_temp)
                for link_children in children_temp:
                    if self.tree_data[0].get(link_children) is None:
                        return False
            self.parents_level = current_children   
        return True

    def run(self):
        dato = 10
        level = 0
        cont = 0
        while(level < dato):
            cont += 1
            if self.next_level():
                level += 1
            
            if(cont>100):
                break;
        
        print("Level ", level)



def get_max_links(self):
    ac = 1
    mul = 1
    for i in range(self[0]):
        pow = i + 1
        mul = self[1]**pow
        ac+= mul
    return ac


print(get_max_links([3,2]))