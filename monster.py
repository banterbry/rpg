import random
import time

class Monster:
	'''
	Container for all monsters. Every monster has a special attack pattern, represented by 'A' or 'B'.
	'A' - attack
	'B' - block
	'''
	monsters = { # hp, attack, speed
	"Arachnid" : [200,50,5],
	"Basilisk" : [200,60,8],
	"Minotaur" : [300,70,20]
	}
	patterns = {
	"Arachnid" : "bab",
	"Basilisk" : "aaa",
	"Minotaur" : "baa"
	}
	message = {
	"Arachnid" : ["The Arachnid stabs you with its poisonous fangs.","The Arachnid hides behind its web."],
	"Basilisk" : ["The Basilisk turns its petrifying gaze towards you...","The Basilisk slithers into the pipes..."],
	"Minotaur" : ["The Minotaur charges you with its horns.", "The Minotaur attempts to parry with its horns..."]
	}
	drops = {
	"Arachnid" : ["health potion"],
	"Basilisk" : ["strength potion","health potion"]
	}
	def __init__(self,name):
		self.name = name
		self.hp = self.monsters[self.name][0]
		self.attack = self.monsters[self.name][1]
		self.speed = self.monsters[self.name][2]
		self.pattern = self.patterns[self.name]

	def display_stats(self):
		print(self.name)
		print("HP: {}".format(self.hp))
		print("Attack: {}".format(self.attack))
		print("Speed: {}".format(self.speed))

	def show_message(self,idx):
		'''
		0 - Attack
		1 - Block
		'''
		print(self.message[self.name][idx])

	def fight(self): # returns the damage dealt by the monster
		damage = random.randint(int(self.attack*0.8),int(self.attack*1.2))
		return damage

	def drop(self): # displays the loot from killing the monster
		for i in self.drops[self.name]:
			print("The {} dropped a {}!".format(self.name,i))
		return self.drops[self.name]
