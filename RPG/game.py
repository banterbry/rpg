import random
import time
from items import Item
from player import Player
from monster import Monster

def flush():
	'''
	A utility function to make the game interface less cluttered
	'''
	print()
	print('-'*10)


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



