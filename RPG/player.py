import random
import time
from items import Item

class Player:
	def __init__(self,name,game):
		self.name = name 
		self.game = game
		self.hp = 100
		self.attack = 20
		self.speed = 10	
		self.inventory =  {}
		self.location = (0,0)
		self.prev = (0,0)
		self.battle = 0	
		self.collected = [0,0]
		self.die = 0
		self.battle_history = {	# to check if a the player has already completed a particular fight
		(2,1) : 0,
		(2,3) : 0,
		(4,4) : 0
		}
		self.cooldown = 0	# block cooldown
		self.weapon = 0

	def show_inv(self):
		print("\nName: {}".format(self.name))
		print("HP: {}".format(self.hp))
		print("Attack: {}".format(self.attack))
		print("\nInventory: ")
		for i in self.inventory:
			print("{}x {}".format(self.inventory[i],i))

	def battle_ui(self):
		print(self.name)
		print("HP: {}".format(self.hp))
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
		The x,y coordinates are stored in a tuple. 
		Since a tuple is immutable, 
		it is converted into a list before being updated and converted back into a tuple.
		'''
		orig = self.location # original location
		lst = list(self.location)
		lst[0] += x
		lst[1] += y
		self.location = tuple(lst)
		if (self.location not in self.game.game_map): # in the event that there is no room at that coordinate
			self.location = orig
		else:
			self.prev = orig
			
	def block(self):
		print("You raise your shield to block it\'s attack!")
		self.cooldown = 1

	def get_damage(self): # returns the damage the player delas
		base_damage = self.attack * Item.items["sword"][0]
		return random.randint(int(base_damage*0.8),int(base_damage*1.2))

	def show_message(self): # show attack message
		print("You attack with your sword.")

	def use_potion(self):
		self.show_inv()
		while (1):
			print("Enter the name of the item: (q) to quit")
			option = input('>')
			if (option.lower()=='q'): return
			if (option not in self.inventory): print("Invalid option!")
			else: break
		print()
		if (Item.items[option][2]=='p'):
			print("You use your {}".format(option))
			if (option=="health potion"):
				self.hp += 100
				print("You gained 100 hp.")
			else:
				self.attack += 5
				print("You gained 5 attack.")
			self.inventory[option]-=1
			if (self.inventory[option]<=0):
				del self.inventory[option]
		else:
			print("What do you plan to do with your sword now...")
		
