import random
import time

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