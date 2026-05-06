import pygame
import random
import sys
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.init()
pygame.font.init()

WIDTH, HEIGHT = 300,600
GRID_SIZE = 25
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

WHITE = (255,255,255)
RED = (240,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,255,255)
PURPLE = (255,50,255)
BLACK = (0,0,0)
COLORS = [RED,GREEN,PURPLE,YELLOW,BLUE,WHITE]

SHAPES = [
    [ #square
        #pos 1
		[
            '.....',
            '.....',
            '.00.',
            '.00..',
            '.....'
		]
	], #end Square

    [ #LONG BAR
        #pos 1
        ['.....',
    	'.....',
    	'0000.',
    	'.....',
		'.....'
		],
	   
	   #pos 2
	   [
		'.....',
    	'..0..',
    	'..0..',
    	'..0..',
    	'..0..'
        ]
        
	   ], # end Long Bar
    
	[ # small T
        #pos 1
        [
            '.....',
        	'..0..',
        	'.000.',
        	'.....',
	        '.....'
		],

	#pos 2
	[
            '.....',
        	'..0..',
         	'..00.',
         	'..0..',
         	'.....'
		  ],
		 #pos 3
		[
            '.....',
          	'.....',
         	'.000.',
        	'..0..',
        	'.....'
		],
          
		  #pos 4
		[
            '.....',
         	'..0..',
         	'.00..',
        	'..0..',
         	'.....'
		 ]

	], #end short T shape
    
	[ # L
        #pos 1
        [
            '.....',
            '.0...',
            '.0...',
            '.00..',
            '.....'
		],
        #pos 2
 		[
			'.....',
			'.....',
            '.000.',
            '.0...',
            '.....'
		],

         #pos 3
        [
            '.....',
            '.00..',
            '..0..',
            '..0..',
            '.....'
		],
         #pos 4
 		[
            '.....',
            '...0.',
            '.000.',
            '.....',
            '.....'
		]
	],# end L shape
    
	[ # Inverse L
        #pos 1
		[
			'.....',
			'..0..',
			'..0..',
			'.00..',
			'.....'
		],


		#pos 2
		[
            '.....',
         	'.0...',
         	'.000.',
        	'.....',
         	'.....'
		 ],
		 #pos 3
		  [
			  '.....',
			  '..00.',
			  '..0..',
			  '..0..',
			  '.....'
		  ],
		#pos 4
		[
            '.....',
        	'.....',
         	'.000.',
         	'...0.',
         	'.....'
		  ]
	],#end inverse L

	# Z Shape
	[
		#pos 1
		[
			'.....',
			'.00..',
			'..00.',
			'.....',
			'.....',
		],

		#pos 2
		[
			'.....',
			'..0..',
			'.00..',
			'.0...',
			'.....',
		]
	], #end Z shape

	#Inverse Z
	[
		#pos 1
		[
			'.....',
			'..00.',
			'.00..',
			'.....',
			'.....',
		],

		#pos 2
		[
			'.....',
			'..0..',
			'..00.',
			'...0.',
			'.....',
		]
	] #end inverse Z shape

] # end all shapes

class TetrisBlock:
	#create new instance of a Block
	def __init__(self,x,y,shape):
		self.x = x
		self.y = y
		self.shape = shape
		self.color = random.choice(COLORS)
		#start at initial position
		self.rotation = 0

class Tetris:
	# create new instance of Tetris game
	def __init__(self,width,height):
		self.width = width
		self.height = height
		#create an empty grid
		self.grid = [[0 for _ in range(width)] for _ in range(height)]
		self.current_block = self.new_block()
		self.game_over = False
		self.lock_delay = 300
		self.lock_timer = 0

	# create a new block with random color
	def new_block(self):
		shape = random.choice(SHAPES)
		block = TetrisBlock(self.width // 2 ,0,shape)
		#check if it's at the top of the grid
		if not self.valid_move(block,0,0,0):
			#end the game if it's at the top
			self.game_over = True
		#return this new block
		return block

	#check if the move given is valid
	def valid_move(self,block,x,y,rotation):
		#get the block's rotation position
		shape = block.shape[( block.rotation + rotation) % len(block.shape)]

		#for each row in the shape
		for i, row in enumerate(shape):
			#for each cell in the row
			for j, cell in enumerate(row):
				#check all the places a block is present in grid and check if it's not at the edges
				if cell == '0' :
					new_x = block.x + j + x
					new_y = block.y + i + y

					#if block wants to move past the edges or at the bottom move is invalid
					if new_x < 0 or new_x >= self.width or new_y >= self.height:
						return False
					#if block is isnt at the top and slot is filled, move is invalid
					elif new_y > 0 and self.grid[new_y][new_x] != 0:
						return False
					#if block is at the top and slot is filled then the game is over.
					elif new_y == 0 and self.grid[new_y][new_x] != 0:
						self.game_over = True
						return False

		#block is in bounds and not touching another block, move is valid.
		return True

	#if all the slots in x-axis is full then clear the line and move all blocks down to next filled position.
	def clear_lines(self):
		lines_cleared = 0
		# for each item in the grid starting at the bottom check if it's full
		i = len(self.grid)-1
		while i >= 0:
			if all(cell !=0 for cell in self.grid[i]):
				#all slots are full, add to lines_cleared and remove that section from grid and fill with empty slots.
				del self.grid[i]
				lines_cleared += 1
				self.grid.insert(0,[0 for _ in range(self.width)])
			else:
				i -= 1
		return lines_cleared
	
	def lock_block(self,block):
		#get the block shape and rotation position
		shape = block.shape[block.rotation % len(block.shape)]

		#go through the rows of shape
		for i,row in enumerate(shape):
			#go through cells of row
			for j, cell in enumerate(row):
				#check if cell is part of block
				if cell == '0':
					#color in block
					self.grid[block.y + i][block.x + j] = block.color
		#check how many lines were cleared
		lines_cleared = self.clear_lines()
		self.current_block = self.new_block()
		#if block has reached the bottom, lock its position and return the number of lines cleared
		return lines_cleared
	
	def update(self,dt):
		#check if the game is done
		if not self.game_over:
			#if the block can move down, update its position
			if self.valid_move(self.current_block, 0, 1, 0):
				# reset the lock timer
				self.lock_timer = 0
				return
			# if block cant move down, start the delay timer
			self.lock_timer += dt #time since last frame
			#if timer passes delay, lock the position
			if self.lock_timer > self.lock_delay:
				self.lock_block(self.current_block)
				self.lock_timer = 0

	#draw the blocks based on it's color and grid size.
	def draw(self):
		for y, row in enumerate(self.grid):
			for x, cell in enumerate(row):
				if cell:
					pygame.draw.rect(screen,cell,
									 (x*GRID_SIZE,y*GRID_SIZE,GRID_SIZE-1,GRID_SIZE-1))
		block  = self.current_block
		shape = block.shape[block.rotation % len(block.shape)]

		#for each row and cell in the block. check if part of the block is there and color it in at it's position.
		for i,row in enumerate(shape):
			for j, cell in enumerate(row):
				if cell == '0':
					pygame.draw.rect(screen,block.color,((self.current_block.x + j) * GRID_SIZE,
																(self.current_block.y + i) * GRID_SIZE,
																GRID_SIZE-1, GRID_SIZE-1))

	#game is already over, reset the grid and restart the game empty.
	def reset(self):
		self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
		self.current_block = self.new_block()
		self.game_over = False

#when game is over print text at the top and offer to restart the  game.
def draw_game_over(screen, x, y):
	#Draw the game over text on the screen
	font = pygame.font.Font(None, 32)
	text = font.render("Game Over", True, RED)
	screen.blit(text, (x, y))
	text = font.render(f"PRESS 'r' to RESTART.", True, RED)
	screen.blit(text, (x,y+50))


#start game
def main():
	# create a window named Tetris, start a clock and initiate the game.
	screen = pygame.display.set_mode((WIDTH,HEIGHT))
	pygame.display.set_caption('Tetris')
	clock = pygame.time.Clock()
	game = Tetris(WIDTH //GRID_SIZE , HEIGHT //GRID_SIZE)

	#how fast the block moves dowm, in milliseconds.
	fall_time = 0
	fall_speed = 100

	# for continuous movement, the delay for intermittent shifting.
	move_time = 0
	move_delay = 100

	while True:
		#make background black
		screen.fill(BLACK)

		#get inputs from the keyboard
		for event in pygame.event.get():

			# SINGLE PRESS ACTIONS

			#if users clicks the x on the window, close the window.
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			#if user presses r, restart the game.
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					if game.game_over:
						game.reset()

				#if user presses up arrow, rotate the block
				if event.key == pygame.K_UP:
					if not game.game_over:
						if game.valid_move(game.current_block, 0, 0, 1):
							game.current_block.rotation += 1  # rotate the block
							game.lock_timer = 0

				#if user presses spacebar, drop the block to the lowest position.
				if event.key == pygame.K_SPACE:
					if not game.game_over:
						while game.valid_move(game.current_block, 0, 1, 0):
							game.current_block.y += 1
						game.lock_block(game.current_block)

		dtime = clock.tick(100)  # get milliseconds since last frame
		fall_time += dtime

		#CONTINUOUS PRESS ACTIONS

		keys = pygame.key.get_pressed()

		if not game.game_over:
			move_time += dtime
			if move_time > move_delay:

				#if user holds down left, keep moving block left.
				if keys[pygame.K_LEFT]:
					if game.valid_move(game.current_block, -1, 0, 0):
						game.current_block.x -= 1
						game.lock_timer = 0

				#if user holds down right, keep moving block right.
				if keys[pygame.K_RIGHT]:
					if game.valid_move(game.current_block, 1, 0, 0):
						game.current_block.x += 1
						game.lock_timer = 0

				#if user holds down right, move block down faster.
				if keys[pygame.K_DOWN]:
					if game.valid_move(game.current_block, 0, 1, 0):
						game.current_block.y += 1
						game.lock_timer = 0
				move_time = 0



			if not game.game_over:
				if fall_time >= fall_speed:
					fall_time = 0
					if game.valid_move(game.current_block, 0, 1, 0):
						game.current_block.y += 1
					else:
						game.update(dtime)
				else:
					game.update(dtime)
		#update the block if game is ongoing every frame.



		game.draw()

		#when game ends, display text and offer restart.
		if game.game_over:
			draw_game_over(screen, 0 , 0)
		pygame.display.flip()


if __name__ == '__main__':
	main()
