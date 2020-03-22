
import random
import time

def flush():
	'''
	A utility function to make the game interface less cluttered
	'''
	print()
	print('-'*10)

class Item:
	'''
	Damage range: Base * 5/6,Base * 6/5
	Character is used to distinguish between potions and weapons
	'''
	items = {
	"Sword" : [5,1,'w'],
	"Bow" : [3,5,'w'],
	"Dagger" : [2,10,'w'], 
	"Potion of Health" : [30,0,'p'], 	
	"Potion of Strength" : [0,20,'p']
	}
	def __init__(self,name,count):
		self.id = name
		print("You have obtained {}x {}".format(count,self.id))
		if (self.items[self.id][2] == 'w'):
			self.damage = self.items[self.id][0]
			self.range = self.items[self.id][1]

class Monster:
	'''
	Container for all monsters. Every monster has a special attack pattern.
	E.g. (attack,attack,block)
	'''
	monsters = {
	"Arachnid" : [200,40,5],
	"Basilisk" : [200,50,15]
	}
	patterns = {
	"Arachnid" : "bab",
	"Basilisk" : "aaa"
	}
	message = {
	"Arachnid" : ["The Arachnid stabs you with its poisonous fangs.","The Arachnid hides behind its web."],
	"Basilisk" : ["The Basilisk turns its petrifying gaze towards you...","The Basilisk slithers into the pipes..."]
	}
	def __init__(self,name):
		self.name = name
		self.hp = self.monsters[self.name][0]
		self.attack = self.monsters[self.name][1]
		self.speed = self.monsters[self.name][2]
		self.pattern = self.patterns[self.name]

	def display_stats(self):
		print(self.name)
		print("HP: {}/{}".format(self.hp,self.monsters[self.name][0]))
		print("Attack: {}".format(self.attack))
		print("Speed: {}".format(self.speed))

	def show_message(self,idx):
		'''
		0 - Attack
		1 - Block
		'''
		print(self.message[self.name][idx])

	def fight(self):
		damage = random.randint(int(self.attack*0.8),int(self.attack*1.2))
		return damage

class Player:
	def __init__(self,name,game):
		self.name = name 
		self.game = game
		self.hp = 100
		self.attack = 20
		self.speed = 10
		self.coins = 50
		self.inventory =  {"Sword" : 1}
		self.location = (2,3)
		self.battle = 0	
		self.collected = [0,0]
		self.battle_history = {	# to check if a the player has already completed a particular fight
		(1,3) : 0,
		(2,3) : 0
		}
		self.cooldown = 0	# block cooldown
		self.weapon = 1

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
		if (Item.items[name][2]=='w'): self.weapon = 1
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
		self.cooldown = 1

	def use_item(self):
		self.show_inv()
		while (1):
			print("Enter the name of the item: ")
			option = input('>')
			if (option not in self.inventory): print("Invalid option!")
			else: break
		print()
		if (Item.items[option][2]=='w'):
			print("You attack with your {}.".format(option))
			base_damage = self.attack * Item.items[option][0]
			return random.randint(int(base_damage*0.8),int(base_damage*1.2))
		else:
			print("You use a {}.".format(option))


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
		(1,3) : ["You come face to face with an Arachnid.","The grotesque remains of the demon lies still. Passage ways opens to the North and East."],
		(1,4) : "trap",
		(2,3) : ["You come face to face with a Basilisk.","The grotesque remains of the serpent lies still."],
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
		print("x - interact\nh - help\ni - inventory\npick - Pick up item\nuse <item name> - Use an item")
		print("Combat: ")

	def show_description(self):
		if (self.player.location == (0,2)): 
			print(self.game_map[self.player.location][self.player.collected[0]])
			return
		if (self.player.location in self.battle_pos):
			already = self.player.battle_history[self.player.location]
			print(self.game_map[self.player.location][already])
			if (not already): 
				self.player.battle = 1
		else:
			print(self.game_map[self.player.location])
	
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
		Options for player in battle:
		1. Attack 2. Block 3. Run
		'''
		valid = ['1','2','3']
		victor = ''
		turn = -1
		monster = Monster(name)
		first = 1 if self.player.speed > monster.speed else 0
		while (self.player.battle):
			turn += 1
			flush()
			monster.display_stats()
			print()
			self.player.battle_ui()
			while (1): # getting the player's action
				option = input('>')
				if (option not in valid): print("Invalid option!")
				else:
					if (option=='1'):
						if (not self.player.weapon): print("You have no weapons!")
						else: break
					elif (option=='2'):
						if (self.player.cooldown): print("You are too exhausted to attempt another block!")
						else: break
					elif (option=='3'):
						print("You live to fight another day...")
						self.player.battle = 0
						break
			if (not self.player.battle): break # if the player abandons the battle
			player_damage = 0
			monster_damage = 0
			monster_move = monster.pattern[turn%3]
			if (monster_move=='b' and option=='2'): # in the event that both player and monster try blocking
				print("The {} tries to block your block...".format(name))
				self.player.cooldown = 1
				continue
			if (self.player.cooldown==1): # cooldown timer for player blocking
				self.player.cooldown = 2
			elif (self.player.cooldown==2):
				self.player.cooldown = 0
			if (first):
				'''---player actions---''' 
				if (option=='1'): 
					player_damage = self.player.use_item()
				if (monster_move == 'b'): 
					monster.show_message(1)
					player_damage //= 3
				if (option=='1'):
					print("Your attack deals {} damage!".format(int(player_damage)))
					monster.hp -= player_damage
				if (monster.hp <= 0):
					victor = 'p'
					self.player.battle = 0
					break	# additional break to fix a bug where the battle was not ending
				'''---monster actions---''' 
				if (monster_move=='b'): continue
				monster_damage = monster.fight()
				if (option=='2'):
					self.player.block()
					monster_damage //= 3
				monster.show_message(0)
				print("The {}\'s attack deals {} damage!".format(name,monster_damage))	
				self.player.hp -= monster_damage
				if (self.player.hp <= 0):
					victor = 'm'
					self.player.battle = 0

			else:
				'''---monster actions---''' 
				if (monster_move == 'a'):
					monster_damage = monster.fight()
				if (option == '2'):
					self.player.block()
					monster_damage //= 3
				'''---player actions---'''
				if (option=='1'):
					player_damage = self.player.use_item()
				if (monster_move =='b'):
					player_damage //= 3
				monster.show_message(0) if (monster_move=='a') else monster.show_message(1)
				print("The {}\'s attack deals {} damage!".format(name,monster_damage))	
				self.player.hp -= monster_damage
				if (self.player.hp <= 0):
					victor = 'm'
					self.player.battle = 0
					break	
				if (option == '1'):
					print("Your attack deals {} damage!".format(int(player_damage)))
					monster.hp -= player_damage
				if (monster.hp <= 0):
					victor = 'p'
					self.player.battle = 0  
					

		if (victor == 'p'):
			print("You have slained the {}. [ENTER] to continue".format(name))
			self.player.battle_history[self.player.location] = 1
		elif (victor == 'm'):
			print("You have been slained by the {}... [ENTER] to continue".format(name))
			self.player.hp = 100
			self.player.location = (0,0)

	def loop(self):
		self.intro()
		self.help()
		while (self.run):
			flush()
			self.show_description()
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
