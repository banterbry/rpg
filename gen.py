import random
import time
import sys
from items import Item
from player import Player
from monster import Monster

player_wins = 0

def generate(which):
	if (which==1):
		st = int(input('>'))
		en = int(input('>'))
		for i in range(st,en+1):
			file = "Testcases/tc{}.txt".format(i)
			sys.stdout = open(file,"w")
			game = Game()
			game.loop()
			sys.stdout.close()
		sys.stdout = open("game.py","a")
		print("# Generated testcases from {} to {}. Player wins {} times.".format(st,en,player_wins))
		sys.stdout.close()
	elif (which==2):
		cnt = 0
		while (not player_wins):
			file = "Testcases/player_win.txt"
			sys.stdout = open(file,"w")
			game = Game()
			game.loop()
			sys.stdout.close()
			cnt += 1
		sys.stdout = open("game.py","a")
		print("# Generated {} testcases.".format(cnt))

def random_string():
	s = ""
	for i in range(10):
		s += chr(random.randint(97,122))
	return s.capitalize()

def flush():
	'''
	A utility function to make the game interface less cluttered
	'''
	print()
	print('-'*10)

def typewrite(s):
	# typewriting effect
	for i in s:
		print(i,end='')
		sys.stdout.flush() 
		# time.sleep(0.03)
	print()

class Game:
	def __init__(self):
		self.player = Player(random_string(),self)
		print("What is your name?")
		print("Input: {}".format(self.player.name))
		self.run = 1
		self.damage_to = 0
		self.damage_from = 0
		self.traps = [(2,5)]
		self.battle_pos = { # locations of monsters
		(2,1) : "Arachnid",
		(2,3) : "Basilisk",
		(4,4) : "Minotaur"
		}
		self.game_map = { # stores all the map descriptions in a dictionary, with coordinates as the key
		(0,0) : "The gates to the Labyrinth looms infront of you. Torches illuminate it on either side.",
		(0,1) : "A dim glow emits from the north bound passage. The passage to the east and west are dark.",
		(0,2) : ["A towering figure appears in front of you. [x]","The room appears to be empty."],
		(-1,1): ["There appears to be a wooden chest lying on the ground. [x]","The chest is empty."],
		(1,1) : "You have entered a narrow passage way. The path to the east looks menacing...",
		(2,4) : "The roof begins to cave in... Something doesn\'t feel right. There are paths to the north and east.",
		(2,1) : ["You come face to face with an Arachnid.","The grotesque remains of the demon lies still. A passage way suddenly appears to the North."],
		(2,5) : "You fall into a pit of lava. You die.",
		(2,3) : ["You come face to face with a Basilisk.","The grotesque remains of the serpent lies still. The passage to the north extennds."],
		(3,4) :	"Something is wrong. You feel as if you are constantly being watched... it isn't too late to turn back. Continue on your journey East or- Oh, a passage to the north!",
		(4,4) : ["Menacing...\nYou come face to face with a Minotaur","The reamins of that wretched creature is scattered around."],
		(3,5) : "This, is a dead end.",
		(2,2) : "You sense something... something slithering in the walls of the chamber... the path leads on North"
		}

		self.movement = ['n','e','w','s','x','use']
		self.combat = ['1','2','3']


	def intro(self):
		typewrite("Welcome to the Labyrinth, {}.".format(self.player.name))
		# time.sleep(0.5)
		typewrite("Find your way through the maze, and defeat the mighty Minotaur.")
		# time.sleep(1)
		typewrite("Good luck...\n")

	def end_screen(self,win):
		print()
		if (win):
			print("Good work, {}. You have successfully defeated the Minotaur.\n".format(self.player.name))
		else:
			print("Game over, {}...".format(self.player.name))
		print("Damage dealt: {}".format(self.damage_to))
		print("Damage taken: {}".format(self.damage_from))
		self.run = 0

	def help(self):
		print("Actions: ")
		print("n - move North\ne - move East\nw - move West\ns - move South")
		print("x - interact\nh - help\ni - inventory\npick - Pick up item\nuse - Use an item (only consumables)")

	def show_description(self):
		'''
		(0,2) and (-1,1) are special rooms, with slightly different
		behaviour
		'''
		if (self.player.location == (0,2)): 
			print(self.game_map[self.player.location][self.player.collected[0]])
			return
		elif (self.player.location == (-1,1)):
			print(self.game_map[self.player.location][self.player.collected[1]])
			return
		elif (self.player.location in self.battle_pos):
			already = self.player.battle_history[self.player.location] # if the player has already fought that mosnter
			print(self.game_map[self.player.location][already]) # display the appropriate description
			if (not already): 
				self.player.battle = 1
		else:
			print(self.game_map[self.player.location])
		if (self.player.location in self.traps):
			self.player.die = 1
	
	def interact(self):
		print()
		if (self.player.location == (0,2)):
			if (not self.player.collected[0]):
				typewrite("A booming voice reverberates around the room.")
				typewrite("\"It\'s dangerous to go alone! Take this.\"")
				item = Item("sword",1)
				self.player.collected[0] = 1
				self.player.add_item(item.id)	
		elif (self.player.location == (-1,1)):
			if (not self.player.collected[1]):
				item1 = Item("health potion",1)
				item2 = Item("strength potion",1)
				self.player.collected[1] = 1
				self.player.add_item(item1.id)
				self.player.add_item(item2.id)
		else:
			print("There\'s nothing to interact with!")

	def battle_engine(self,name):
		'''
		Speed determines who moves first.
		Damage dealt by monsters are within a fixed range.
		Player damage = random(attack*weapon*0.8, attack*weapon*1.2)
		Options for player in battle:
		1. Attack 2. Block 3. Run
		'''
		valid = ['1','2','3'] # valid options for the player -> reduces hard coding
		victor = ''
		turn = -1
		monster = Monster(name)
		first = 0
		if (self.player.speed > monster.speed): # who moves first
			first = 1
		while (self.player.battle):
			turn += 1
			flush()
			monster.display_stats()
			print()
			self.player.battle_ui()
			while (1): # getting the player's action
				option = random.choice(self.combat)
				print("Input: {}".format(option))
				if (option not in valid): print("Invalid option!")
				else:
					if (option=='1'):
						if (not self.player.weapon): print("You have no weapons!") # if player has no weapons to attack
						else: break
					elif (option=='2'): # attempts a block
						if (self.player.cooldown): print("You are too exhausted to attempt another block!")
						else: break
					elif (option=='3'): # run from battles
						print("You live to fight another day...")
						self.player.battle = 0
						self.player.location = self.player.prev # sets player location to where it came from before the battle
						flush()
						break
			if (not self.player.battle): 
				self.show_description()
				break # if the player abandons the battle
			player_damage = 0
			monster_damage = 0
			monster_move = monster.pattern[turn%3]
			if (monster_move=='b' and option=='2'): # in the event that both player and monster try blocking
				print("You both attempt blocking... cowards.")
				self.player.cooldown = 1
				continue
			if (self.player.cooldown==1): # increments cooldown
				self.player.cooldown += 1
			elif (self.player.cooldown==2):
				self.player.cooldown = 0
			if (first): # if the player goes first
				'''---player actions---''' 
				if (option=='1'): 
					player_damage = self.player.get_damage()
				if (monster_move == 'b'): 
					monster.show_message(1) # block has higher priority, thus it is shown first
					player_damage //= 3
				if (option=='1'):
					self.player.show_message()
					print("Your attack deals {} damage!".format(int(player_damage)))
					monster.hp -= player_damage
				self.damage_to += player_damage
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
				self.damage_from += monster_damage
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
					player_damage = self.player.get_damage()
				if (monster_move =='b'):
					player_damage //= 3 
				if (monster_move=='a'):
					monster.show_message(0)
					print("The {}\'s attack deals {} damage!".format(name,monster_damage))	
				else:
					monster.show_message(1)
				self.player.hp -= monster_damage
				self.damage_from += monster_damage
				if (self.player.hp <= 0):
					victor = 'm'
					self.player.battle = 0
					break	
				if (option == '1'):
					self.player.show_message()
					print("Your attack deals {} damage!".format(int(player_damage)))
					monster.hp -= player_damage
				self.damage_to += player_damage	
				if (monster.hp <= 0):
					victor = 'p'
					self.player.battle = 0  
		self.player.cooldown = 0 # reset block cooldown after every battle
		if (victor == 'p'):
			print("You have slained the {}. [ENTER] to continue\n".format(name))
			self.player.battle_history[self.player.location] = 1
			if (name=="Minotaur"): return # Minotaur has no drops, prevents key error
			drops = monster.drop()
			for i in drops:
				self.player.add_item(i)
		elif (victor == 'm'):
			print("You have been slained by the {}...".format(name))
			self.player.die = 1

	def loop(self): # Main game loop
		global player_wins
		self.intro()
		self.help()
		while (self.run):
			flush()
			if (self.player.battle_history[(4,4)]==1): # if player completed the final fight
				self.end_screen(1)
				player_wins += 1
				break
			self.show_description()
			if (self.player.battle): # if the player has entered battle
				self.battle_engine(self.battle_pos[self.player.location])
			if (self.player.die):
				self.end_screen(0)
				break
			action = random.choice(self.movement)
			print("Input: {}".format(action))
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
			elif (action == "use"):
				self.player.use_potion()

if "__main__" == __name__:
	generate(1)

# Generated testcases from 1 to 100. Player wins 0 times.
# Generated 478 testcases.
# Generated 1202 testcases.
# Generated testcases from 101 to 500. Player wins 1 times.
