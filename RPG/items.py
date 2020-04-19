import random
import time

class Item:
	'''
	Base damage = weapon attack * player attack
	Damage range: base* 5/6, base * 6/5
	Character is used to distinguish between potions and weapons
	'''
	items = {
	"sword" : [4,1,'w'], 
	"health potion" : [30,0,'p'], 	
	"strength potion" : [0,20,'p']
	}
	def __init__(self,name,count):
		self.id = name
		print("You have obtained {}x {}".format(count,self.id))
		if (self.items[self.id][2] == 'w'):
			self.damage = self.items[self.id][0]
			self.range = self.items[self.id][1]
