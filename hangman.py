import pyglet
import random
from pyglet.window import key


window = pyglet.window.Window()
# making a list of all the values from [97,122]
list_of_ascii_values = [x for x in range(97,123)]
print list_of_ascii_values
# The keys to the diccionary are the integers between [97,122], 
# and the values their character equivalents
dic_keys = {}
for ascii_key in list_of_ascii_values:
	dic_keys[ascii_key] = chr(ascii_key)

ifs = open("hangman_words.txt", 'r')
all_words = []
#read all of the words from a file
for w in ifs.read().split():
	all_words.append(w)

# Sort the x Coordinates to be passed to the Tile objects
x_coords = [2.0, 1.8, 1.64, 1.5,1.4, 4.3, 3.5, 3.0, 2.55, 2.25]
x_coords.sort(reverse= True)

class Tile:
	
	def __init__(self, my_char, my_x):
		self.my_char = my_char
		self.x = my_x
		self.uncovered = 0 #if uncovered then 1
		self.label = pyglet.text.Label('-',
										font_name='Times New Roman',
										font_size=36,
										x=window.width//self.x, y=window.height//4)
	def update(self, input_char):
		if self.uncovered:
			return 0 
		if input_char.upper() == self.my_char:
			self.uncovered = 1
			self.label = pyglet.text.Label(input_char,
											font_name='Times New Roman',
											font_size=36,
											x=window.width//self.x, y=window.height//4)
			return 1
		return 0

	def draw(self):
		self.label.draw()
		return self.uncovered 

class Driver:
	
	def __init__(self):
		# choose a random word from the list of all_words 
		self.word = all_words[random.randint(0,len(all_words)-1)]
		self.total_strikes = len(self.word)*2
		self.total_strikes_label = pyglet.text.Label(str(self.total_strikes),
									font_name='Times New Roman',
									font_size=25,
									x=window.width//1.15, y=window.height//2,
									anchor_x='right', anchor_y='center')
		self.current_strikes = 0
		self.current_strikes_label = pyglet.text.Label('0',
									font_name='Times New Roman',
									font_size=25,
									x=window.width//1.63, y=window.height//2,
									anchor_x='right', anchor_y='center')
		self.tiles = []
		curr_x_coord = 0
		# Accumulate all of the Tile objects that are going to be displayed in the screen
		for c in self.word:
			# the Tile requires both the character that it will be covering,
			# and the x coordinate where the label should be plotted
			t = Tile(c,x_coords[curr_x_coord])
			self.tiles.append(t)
			curr_x_coord += 1

	def update(self, input_char):
		total_uncovered = 0
		for t in self.tiles:
			# add up all of the Tiles that where uncovered for the first time during this round
			total_uncovered += t.update(input_char)
		if total_uncovered == 0:
			self.current_strikes += 1
			self.current_strikes_label = pyglet.text.Label(str(self.current_strikes),
									font_name='Times New Roman',
									font_size=25,
									x=window.width//1.63, y=window.height//2,
									anchor_x='right', anchor_y='center')

	def draw(self):
		player_won = 0
		for t in self.tiles:
			player_won += t.draw()
		# if all of the Tiles have been uncovered
		if player_won == len(self.word):
			label_won = pyglet.text.Label('You won!',
						font_name='Times New Roman',
						font_size=36,
						x=window.width//2, y=window.height//2.5,
				        anchor_x='center', anchor_y='center')
			
			label_won.draw()
		
		if self.current_strikes >= self.total_strikes:
			label_lose = pyglet.text.Label("You lost!",
									font_name='Times New Roman',
									font_size=25,
									x=window.width//2, y=window.height//2.5,
									anchor_x='right', anchor_y='center')
			label_lose.draw()
			
		self.total_strikes_label.draw()
		self.current_strikes_label.draw()

	
# Static labels that are not dynamically updated during the program
label = pyglet.text.Label('Hangman Game',
						font_name='Times New Roman',
						font_size=36,
						x=window.width//2, y=window.height//1.2,
				        anchor_x='center', anchor_y='center')

number_of_strikes = pyglet.text.Label('Number of Strikes',
									font_name='Times New Roman',
									font_size=25,
									x=window.width//1.9, y=window.height//2,
									anchor_x='right', anchor_y='center')
out_of = pyglet.text.Label('out of',
							font_name='Times New Roman',
							font_size=25,
							x=window.width//1.3, y=window.height//2,
							anchor_x='right', anchor_y='center')

# testcases 1, testing the Tile constructor method:
try:
	mytile = Tile()
except:
	print "You need to provide parameters for the constructor."

# testcases 2, testing the Driver constructor method:
try:
	mydriver = Driver("jsfjsd")
except:
	print "The driver takes no parameters"

driver = Driver()
@window.event
def on_draw():
	window.clear()
	label.draw()
	number_of_strikes.draw()
	out_of.draw()
	driver.draw()
	
@window.event
def on_key_press(symbol, modifiers):
	if symbol in dic_keys:
		driver.update(dic_keys[symbol])
	elif symbol == key.RETURN:
			window.close()

pyglet.app.run()


