import board

class Player():
	def __init__(self, color, tile):
		#color: black(X) or white(O)
		#tile: 1(X) or 0(O) 
		self.color = color
		self.tile = tile
	def makeRemove(self, from_coor, board):
		#make a remove at selected location
		(x,y) = from_coor
		board.set(x, y, -1)
	def makeMove(self, from_coor, to_coor, board):
		#make a move from one location to another
		from_tile = board.get(from_coor[0], from_coor[1])
		board.set(from_coor[0], from_coor[1], -1)
		board.set(to_coor[0], to_coor[1], from_tile)
	def findRemove(self):
		pass #override
	def findMove(self):
		pass #override
	def isWin(self, board):
		# You win when your opponent has nothing to move
		opponent = (self.tile+1)%2
		return board.checkMovesLeft(opponent) == 0

class HumanPlayer(Player):
	def findRemove(self):
		#ask user for coordinates to remove
		#check if valid
		#if valid, return it
		pass
	def findMove(self):
		#ask user for inputs (from and to)
		#check if inputs are valid
		#if valid, return the two coordinates
		pass



class AIPlayer(Player):
	def findRemove(self):
		#ranodm select from the legal ones 
		#remember to check tile
		#return a selected coordinates
		pass
	def findMove(self, strat=miniMax, board):
		#call miniMax to find a movement
		#return that move
		pass

	#static functions (OR NOT, IF YOU DON'T WANT)
	def miniMax(): ####MODIFY THIS HOWEVER YOU WANT
		pass

	def alphaBetaPrunning(): ####MODIFY THIS HOWEVER YOU WANT
		pass

	


