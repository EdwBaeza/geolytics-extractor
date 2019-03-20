class Tree:
	""" Class Tree convert a dictionary and a Keys_List in an Iterable Tree
	for control the movement in the tree """

	def __init__(self, dictionary, Keys_List):

		#attributes of the class
		self.dictionary_copy = dictionary
		self.Keys_List_copy = Keys_List

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
		if link == self.Keys_List_copy[0]:
			father = 1   #Doesn't exist father because you're in the seed
		else:
			for value in self.Keys_List_copy:
				children = self.dictionary_copy[value]
				if link in children:
					Children_Position = children.index(link)
					father = value
					break
		return father

	def get_Initial_Position(self):
		print("INITIAL POSITION:")
		if ( self.search_father(self.Initial_Position) == 1) :
			#we are in the seed, we don't have a father
			print("Seed\n")
		else:
			number_node = self.Keys_List_copy.index(self.Initial_Position)
			Node = "Node_" + str(number_node)
			name_father = self.search_father(self.Initial_Position)
			number_node_father = self.Keys_List_copy.index(name_father)
			if name_father == "seed":
				print("Son of the seed")
			else:
				print("Son of the Node_" + str(number_node_father) )
			print("Current position: ", Node + "\n")

	def Get_Back_Position(self):
		print("BACK POSITION:")
		Posible_Position = self.search_father(self.Initial_Position)
		if Posible_Position == 1:
			#we are in the seed, we don't have a father
			print("Doesn't exist a back position, because you're in the seed\n")
		else:
			number_father = self.Keys_List_copy.index(Posible_Position)
			if number_father == 0:
				print("Father is the seed\n")
			else:
				Father = 'Node_' + str(number_father) +"\n"
				print("Father is the " + Father)

	def Get_Front_Position(self):
		print("FRONT POSITION:")
		#use this function before that use the Advance_One_Position Function
		print(self.Front_Position)
		print()

	def Back_One_Position(self, flag):
		#Search the father of the generation and move to there
		if (flag == 0):
			#we aren't want to back one position
			data = self.search_father(self.Initial_Position)
			if data == 1:
				print("Doesn't exist a back position, because you're in the seed\n")
			else:
				self.Back_Position = data
		else:
			#we want to back one position when flag is 1
			data = self.search_father(self.Initial_Position)
			if data == 1:
				print("Doesn't exist a back position, because you're in the seed\n")
			else:
				self.level -= 1 #this not should pass if I only want to know the back position without do the movement
				self.update_The_Positions(data)
		
	def update_The_Positions(self, Position):

		level_flag = 0
		self.Initial_Position = Position #is a string with the link
		self.Back_One_Position(level_flag) #we want only update the back position when level_flag is 0
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
		"""how we have a list of children, this function should receive a number of son for decide to where advance 
		son_number is the index number of the list shown by Get_Front_Position"""
		
		next_son = self.Front_Position_Copy[son_number] #next_son is a string with the link
		self.level += 1
		#update the Positions
		self.update_The_Positions(next_son)

	def Advance_To_Siblings(self, sibling_number):
		#Search for a position in the same children generation
		#sibling_number is the index number of the list shown by Get_Front_Position"""
		father = self.search_father(self.Initial_Position)
		if father == 1:
			print("doesn't exist siblings, because you're in the seed")
		else:
			list_of_siblings = self.dictionary_copy[father]
			next_position = list_of_siblings[sibling_number]
			print("My position in this moment is: ")
			self.get_Initial_Position()

			#update the positions
			self.update_The_Positions(next_position)

	def Get_Current_Node(self):
		Number_Node = self.Keys_List_copy.index(self.Initial_Position)
		return print("Current Node: ", Number_Node)

	def Get_Current_Level(self):
		return print("Current level: ", self.level)