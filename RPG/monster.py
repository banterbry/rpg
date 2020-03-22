import random
import time

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
