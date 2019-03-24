class Tree:
	""" Class Tree convert a dictionary and a Keys_List in an Iterable Tree
	for control the movement in the tree """

	def __init__(self, dictionary, Keys_List, abstract_dict):

		#attributes of the class
		self.dictionary_copy = dictionary
		self.Keys_List_copy = Keys_List
		self.abstract_dict_copy =  abstract_dict

		value = 0
		key = Keys_List[value] #The first position is the seed, then we get the first children
		children_list = []

		self.level = 0  #in the initial time we are en the level 0, with the seed
		self.seed = key
		self.Initial_Position = key #the first link that is the seed
		self.Back_Position = "it doesn't exist because you're in the seed"
		self.Back_Position_Copy = "it doesn't exist because you're in the seed"

		#number_children_seed = len(dictionary[key]) #are the number of children of the seed
		#for link in range(number_children_seed):
		#	children_list.append('Son'+str(link))

		children_to_show = dictionary[key]
		for son in children_to_show:
			number_node = self.Keys_List_copy.index(son)
			children_list.append('Node_'+str(number_node))

		self.Front_Position = children_list #save the children of the seed in text format
		self.Front_Position_Copy = dictionary[key] #save a copy of the children of the seed in link format
		#Front_Position and Front_Position_Copy should have the same size

	def search_father(self, link):
		#this method receive a link
		#then, this method search the link father of the link of the parameter
		#this methon return a link, that is the link father
		if link == self.Keys_List_copy[0] :
			father = 1   #Doesn't exist father because you're in the seed
		else:
			for value in self.Keys_List_copy:
				children = self.dictionary_copy[value]
				if link in children:
					Children_Position = children.index(link)
					father = value
					break
		return father #father is a link

	def get_Initial_Position(self):
		#this method doesn't receive anything
		#then, this method search the current link that is the same that the current node
		#return a link
		print("INITIAL POSITION:")
		if ( self.search_father(self.Initial_Position) == 1) :
			#we are in the seed, we don't have a father
			print("Seed\n")
			return None #If there are not a father, return a None
		else:
			current_node = self.Initial_Position #new line
			number_node = self.Keys_List_copy.index(self.Initial_Position)
			Node = "Node_" + str(number_node)
			name_father = self.search_father(self.Initial_Position)
			number_node_father = self.Keys_List_copy.index(name_father)
			if name_father == "seed":
				print("Son of the seed" )
			else:
				print("Son of the Node_" + str(number_node_father) )
			print("Current position: ", Node + "\n")
			return current_node #current_node is a link, this method return a link

	def Get_Back_Position(self):
		#this method doesn't receive anything
		#then, this method try to search a link father for the current link and show it
		#return a link that is the link father or return None if doesn't exist a link fater because you are in the seed
		print("BACK POSITION:")
		Posible_Position = self.search_father(self.Initial_Position)
		if Posible_Position == 1:
			#we are in the seed, we don't have a father
			message = "Doesn't exist a back position, because you're in the seed\n"
			print(message)
			return None #if there are not a father return a None
		else:
			number_father = self.Keys_List_copy.index(Posible_Position)
			if number_father == 0:
				print("Father is the seed\n")
				return self.Keys_List_copy[number_father] #return the seed link
			else:
				return Posible_Position #Posible_Position is a link, this method return a link
				#Father = 'Node_' + str(number_father) +"\n"
				#print("Father is the " + Father)

	def Get_Front_Position(self):
		#this method doesn't receive anything
		#then, this method try to search children of the current link and show it
		#return a list of links that are the children
		print("FRONT POSITION:")
		#use this function before that use the Advance_One_Position Function
		show_children_list = self.Front_Position_Copy[self.Initial_Position]
		print(show_children_list)
		print()
		return show_children_list #is a list ok links, this method return a list of links
		#######################################3

	def Back_One_Position(self, flag):
		#this method receive a flag for indicate a type of action
		#if the flag is 1, then back one position, but the flag is 0, then only update the Back_Position
		#this method doesn't return anything
		if (flag == 0):
			#we aren't want to back one position
			data = self.search_father(self.Initial_Position)
			if data == 1:
				print("Doesn't exist a back position, because you're in the seed\n")
				self.Back_One_Position = None
			else:
				self.Back_Position = data #data is a link
				#In Back_Position save a link
		else:
			#we want to back one position when flag is 1
			data = self.search_father(self.Initial_Position)
			if data == 1:
				print("Doesn't exist a back position, because you're in the seed\n")
			else:
				self.level -= 1 #this not should pass if I only want to know the back position without do the movement
				self.update_The_Positions(data) #data is a link
		
	def update_The_Positions(self, Position):
		#this method receive a link as Position
		#this method establishes the link of the parameter as the current node, 
			#according to this result it establishes the father node and the children
		#this method doesn't return anything
		level_flag = 0
		self.Initial_Position = Position #is a string with the link
		self.Back_One_Position(level_flag) #we want only update the back position when level_flag is 0
		#the Back_position is a link
		self.Back_Position_Copy = 'Father of level ' + str(self.level)

		children_list = []
		#number_children = len() #are the number of children of the seed
		#for link in range(number_children):
		#	children_list.append('Son'+str(link))

		children_to_show = self.dictionary_copy[Position]
		for son in children_to_show:
			number_node = self.Keys_List_copy.index(son)
			children_list.append('Node_'+str(number_node))

		self.Front_Position = children_list  #save the children of the seed in text format
		self.Front_Position_Copy = self.dictionary_copy[Position] #save a copy of the children of the seed in link format

	def Advance_One_Position(self, son_number):
		#this method receive a int number as a son_number
		#this method should receive a number of son for decide to where advance 
			#son_number is the index number of the list shown by Get_Front_Position
		#this method doesn't return anything
		next_son = self.Front_Position_Copy[son_number] #next_son is a string with the link
		self.level += 1
		#update the Positions
		self.update_The_Positions(next_son) #next_son is a link

	def Advance_To_Siblings(self, sibling_number):
		#this method receive a int number as a sibling_number
		#Search for a position in the same children generation and advance there
			#sibling_number is the index number of the list shown by Get_Front_Position
		#this method doesn't return anything
		father = self.search_father(self.Initial_Position)
		if father == 1:
			print("doesn't exist siblings, because you're in the seed")
		else:
			list_of_siblings = self.dictionary_copy[father]
			next_position = list_of_siblings[sibling_number]
			print("My position before move to sibling is: ")
			self.get_Initial_Position()

			#update the positions
			self.update_The_Positions(next_position)

	def Get_Current_Node(self):
		#this method doesn't receive anything
		#then, this method search the current node and show it
		#return an object of type Node
		###Number_Node = self.Keys_List_copy.index(self.Initial_Position)
		current_node = self.abstract_dict_copy[self.Initial_Position]

		#return an object of type node
		return current_node #current_node is an object of type Node

	def Get_Current_Level(self):
		#this method doesn't receive anything
		#then, this method search the current level and show it
		#return an int number that represent the current level
		return self.level

	def Get_data():
		#this method doesn't receive anything
		#then, this method search the current node for return it
		#return an object of type Node or None if is limtied
		result_object = self.abstract_dict_copy.get(self.Initial_Position)
		return result_object