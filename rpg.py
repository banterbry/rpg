import random
import time

class Monster:
	'''
	Container for all monsters. Every monster has a special attack pattern.
	E.g. (attack,attack,block)
	'''
	monsters = {
	"Arachnid" : [250,40,5],
	"Basilisk" : [200,30,15]
	}
	patterns = {
	"Arachnid" : "bab",
	"Basilisk" : "aaa"
	}
	message = {
	"Arachnid" : ["The Arachnid stabs you with its poisonous fangs.","It hides behind its web."],
	"Basilisk" : ["",""]
	}
	def __init__(self,name):
		self.name = name
		self.hp = self.monsters[self.name][0]
		self.attack = self.monsters[self.name][1]
		self.speed = self.monsters[self.name][2]
		self.pattern = self.patterns[self.name]

	def move(self,turn):
		if (self.pattern[turn%3] == 'a'):
			print(self.message[self.name][0])
			damage = random.randint(int(40*0.8),int(40*1.2))
			return damage
		else:
			print(self.message[self.name][1])
			return -1

class Item:
	'''
	Damage range: Base * 5/6,Base * 6/5
	'''
	items = {
	"Sword" : [50,1,'w'],
	"Bow" : [30,5,'w'],
	"Dagger" : [20,10,'w'], 
	"Potion of Health" : [30,0,'p'], 	
	"Potion of Strength" : [0,20,'p']
	}
	def __init__(self,name,count):
		self.id = name
		print("You have obtained {}x {}".format(count,self.id))
		if (self.items[self.id][2] == 'w'):
			self.damage = self.items[self.id][0]
			self.range = self.items[self.id][1]

class Player:
	def __init__(self,name,game):
		self.name = name 
		self.hp = 100
		self.attack = 10
		self.speed = 10
		self.coins = 50
		self.inventory =  {}
		self.location = (1,2)
		self.battle = 0
		self.collected = [0,0]
		self.game = game

	def show_inv(self):
		print("\nInventory: ")
		for i in self.inventory:
			print("{}x {}".format(self.inventory[i],i))

	def battle_ui(self):
		print(self.name)
		print("HP: {}/{}".format(self.hp,100))
		print("Attack: {}".format(self.attack))
		print("Speed: {}".format(self.speed))
		print("Actions:\n1. Attack 2. Block 3. Run")

	def add_item(self,name):
		'''
		A function to add an item to the player's inventory
		'''
		if (name not in self.inventory):
			self.inventory[name] = 1
		else:
			self.inventory[name] += 1

	def update_pos(self,x,y):
		'''
		A function to update the coordinates of the player.
		The x,y coordinates are stored in a tuple. Since a tuple is immutable, 
		it is converted into a list before being updated and converted back into a tuple.
		'''
		orig = self.location # original location
		lst = list(self.location)
		lst[0] += x
		lst[1] += y
		self.location = tuple(lst)
		if (self.location not in self.game.game_map): # in the event that there is no room at that coordiante
			self.location = orig

	def block(self):
		print("You raise your shield to block it\'s attack!")

class Game:
	def __init__(self):
		self.player = Player(input("What is your name?"),self)
		self.run = 1
		self.battle_pos = {
		(1,3) : "Arachnid",
		(2,3) : "Basilisk"
		}
		self.game_map = { # stores all the map descriptions 
		(0,0) : "The gates to the Labyrinth looms infront of you. Torches illuminate it on either side.",
		(0,1) : "A dim glow emits from the passage ahead. The passage to the east and west are dark.",
		(0,2) : ["A towering figure appears in front of you.","The room appears to be empty."],
		(-1,1): "There appears to be a wooden chest lying on the ground.",
		(1,1) : "You have entered a spacious cave system. There is a dim light in the passage to the East.\nDarkness fills the North.",
		(2,1) : "Welcome to the shop! Enter the id of the item you would like to purchase, or -1 to exit.",
		(1,2) : "The roof begins to cave in... Something doesn\'t feel right.",
		(1,3) : "You come face to face with an Arachnid.",
		(1,4) : "trap",
		(2,3) : "monster",
		(3,3) :	"boss"
		}

	def intro(self):
		print("Welcome to the Labyrinth, {}.".format(self.player.name))
		# time.sleep(0)
		print("Find your way through the maze, and defeat the mighty Minotaur.")
		# time.sleep(2.5)
		print("Good luck...\n")

	def help(self):
		print("Actions: ")
		print("n - move North\ne - move East\nw - move West\ns - move South")
		print("x - interact\nh - help\ni - inventory\npick - Pick up item\n use <item name> - Use an item")
		print("Combat: ")
	
	def interact(self):
		print()
		if (self.player.location == (0,2)):
			if (not self.player.collected[0]):
				print("A booming voice reverberates around the room.")
				print("\"It\'s dangerous to go alone! Take this.\"")
				item = Item("Sword",1)
				self.player.collected[0] = 1
				self.player.add_item(item.id)	
		elif (self.player.location == (-1,1)):
			if (not self.player.collected[1]):
				item = Item("Potion of Health",1)
				self.player.collected[1] = 1
				self.player.add_item(item.id)
		else:
			print("There\'s nothing to interact with!")

	def shop(self):
		if (self.player.location == (2,1)):
			pass

	def battle_engine(self,name):
		'''
		Speed determines who moves first.
		Damage dealt by monsters are within a fixed range.
		Player damage = random(attack*weapon*0.8, attack*weapon*1.2)
		'''
		valid = ['1','2','3'] # list of valid options for the player to choose from
		first = 0
		turn = -1
		monster = Monster(name)
		if (self.player.speed > monster.speed):
			first = 1
		while (self.player.battle):
			turn += 1
			print()
			self.player.battle_ui()
			while (1):
				action = input('>')
				if (action in valid):
					break
				else:
					print("Invalid move!")
			if (action=='2'):
				self.player.block()
				continue
			if (first):
				pass
			else:
				if (dmg==-1):
					
				if (action=='1'):
					pass

	def loop(self):
		self.intro()
		self.help()
		while (self.run):
			print()
			print('-'*10) # makes the interface less cluttered
			if (self.player.location == (0,2)):
				print(self.game_map[self.player.location][self.player.collected[0]])
			else:
				print(self.game_map[self.player.location])
			if (self.player.location in self.battle_pos):
				self.player.battle = 1
			if (self.player.battle):
				self.battle_engine(self.battle_pos[self.player.location])
			action = input('>')
			if (action.lower() == 'n'):
				self.player.update_pos(0,1)
			elif (action.lower() == 's'):
				self.player.update_pos(0,-1);
			elif (action.lower() == 'e'):
				self.player.update_pos(1,0);
			elif (action.lower() == 'w'):
				self.player.update_pos(-1,0)
			elif (action.lower() == 'x'):
				self.interact()
			elif (action.lower() == 'i'):
				self.player.show_inv()
			elif (action.lower() == 'h'):
				self.help()

if "__main__" == __name__:
	game = Game()
	game.loop()



