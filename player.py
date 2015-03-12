import board
from copy import deepcopy

class Player():
	def __init__(self, color, tile):
		#color: black(X) or white(O), NOT SURE IF WE NEED IT
		#tile: 1(X) or 0(O) 
		self.color = color
		self.tile = tile
	def makeRemove(self, from_coor, board):
		#make a remove at selected location
		(x,y) = from_coor
		board.set(x, y, -1)
	# +++++ Jia made change below, board use to be the last argument, now, it is the second argument +++++ 
	def makeMove(self,board, from_coor, to_coor):
		#make a move from one location to another
		from_tile = board.get(from_coor[0], from_coor[1])
		board.set(from_coor[0], from_coor[1], -1)
		board.set(to_coor[0], to_coor[1], from_tile)        
	@classmethod
	def executeMove(cls, board, move):
                for i in range(len(move)-1):
                        sx, sy = move[i] #start crd 
                        ex, ey = move[i+1] #end crd
                        value = board.get(sx,sy)
                        board.set(sx,sy,-1) #set start crd to be .
                        #clear up the opponent's tile
                        if(sx==ex):
                                board.set(sx,(sy+ey)/2,-1)
                        elif(sy==ey):
                                board.set((sx+ex)/2,sy,-1)
                        else:
                                print 'Error in ExecuteMove. The move you provide is not valid'
                        board.set(ex,ey,value)

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
		print "Enter the Position (x,y) You Want to Remove."
		x = int(input("Enter x: "))
		y = int(input("Enter y: "))
		#check if valid
		if this.tile == 1: #black tile
			pass
		else: #white tile, needs to check adjacent tiles
			pass
		#if valid, return it
		return (x,y)

		pass
	def findMove(self):
		#ask user for inputs (from and to)
		print "Enter the Position (x1,y1) You Want to Move from."
		x1 = int(input("Enter x1: "))
		y1 = int(input("Enter y1: "))
		print "Enter the Position (x2,y2) You Want to Move to."
		x2 = int(input("Enter x2: "))
		y2 = int(input("Enter y2: "))
		#check if inputs are valid #############
			#NEED TO BE IMPLEMENTED
		#if valid, return the two coordinates
		return [(x1, y1), (x2, y2)]



class AIPlayer(Player):
	def findRemove(self):
		#ranodm select from the legal ones 
		#remember to check tile
		#return a selected coordinates
		pass
	
	def findMove( self, board, depth):
		import state
		s = state.State(deepcopy(board),self.tile)
		move = state.alphabeta(s,depth,self.tile)
		return move
		



