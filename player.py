import board, random
from copy import deepcopy
from ast import literal_eval

class Player():
	def __init__(self, color, tile):
		#color: black(X) or white(O), NOT SURE IF WE NEED IT
		#tile: 1(X) or 0(O) 
		self.color = color
		self.tile = tile
	# def makeRemove(self, board):
	# 	return
	# def makeMove(self, board):
	# 	return
	# def findRemove(self, board):
	# 	return []#override
	# def findMove(self, board):
	# 	return []#override
	def isWin(self, board):
		# You win when your opponent has nothing to move
		opponent = (self.tile+1)%2
		return board.checkMovesLeft(opponent) == 0

# class HumanPlayer(Player):
# 	def findRemove(self, board):
# 		while True:
# 			#ask user for coordinates to remove
# 			print "Enter the Position (x,y) You Want to Remove."
# 			x = int(input("Enter x: "))
# 			y = int(input("Enter y: "))
# 			#check if valid
# 			if this.tile == 1: #black tile
# 				if (x,y) == (8,1) or (x,y) == (1,8) \
# 				or (x,y) == (4,5) or (x,y) == (5,4):
# 					return (x,y)
# 			else: #white tile, needs to check adjacent tiles
# 				if (((x+1, y) == (8,1) or (x,y-1) == (8,1)) and board.get(8,1)==-1) \
# 				or (((x, y-1) == (1,8) or (x+1,y) == (1,8)) and board.get(1,8)==-1) \
# 				or (((x, y) == (4,4) or (x,y) == (5,5)) and (board.get(4,5) == -1 or board.get(5,4)==-1)):
# 					return (x,y)
# 			print "Invalid position. Try again."
		
# 	def findMove(self):
# 		#ask user for list inputs, in form "(x1, y1), (x2, y2), (x3, y3), ...."
# 		while (True):
# 			move_input = input("Enter a list of postions you want to move.")
# 			move_input = list(literal_eval(move_input)) #list of tuples
# 			if len(move_input) < 2 :
# 				continue
# 			me = self.tile
# 			opponent = (self.tile+1)%2
# 			success = 1
# 			for i in range(len(move_input)-1):
# 				(x1,y1) = move_input[i]
# 				(x2,y2) = move_input[i+1]
# 				if (i ==0 and board.get(x1, y1) != me) or \
# 					(i != 0 and board.get(x1, y1) != -1) or \
# 					board.get(x2,y2) != -1 or \
# 					(x1==x2 and abs(y1-y2)!=2) or \
# 					(y1==y2 and abs(x1-x2)!=2) or \
# 					(x1==x2 and board.get(x1,(y1+y2)/2) != opponent) or \
# 					(y1==y2 and board.get((x1+x2)/2, y1) != opponent):
# 						success = 0
# 						break
# 			if success:
# 				return move_input

	



class AIPlayer(Player):
    def __init__(self, color, tile, depth):
        self.color = color
        self.tile = tile
        self.depth = depth

	def makeRemove(self, board):
		print "Making remove..."
		#make a remove at selected location
		(x,y) = self.findRemove(board)
		board.set(x, y, -1)

	def findRemove(self, board):
		print "###########"
		#get legal ones
		legal_moves = []
		if self.tile == 1: #BLACK
			legal_moves = [(8,1), (1,8), (4,5), (5,4)]
		else:#WHITE
			if board.get(8,1) == -1:
				legal_moves = [(7,1), (8,2)]
			elif board.get(1,8) == -1:
				legal_moves = [(1,7), (2,8)]
			else:
				legal_moves = [(4,4), (5,5)]
		#return a random one from legal moves
		random.shuffle(legal_moves)
		print legal_moves
		return legal_moves[0]
	
	def makeMove(self,board):
		#make a move from one location to another
		list_of_moves = self.findMove(board)
		for i in len(list_of_moves)-1:
			(sx, sy) = list_of_moves[i]
			(ex, ey) = list_of_moves[i+1]
			value = board.get(sx,sy)
			board.set(sx,sy,-1) #set start crd to be .
			#clear up the opponent's tile
			if(sx==ex):
				board.set(sx,(sy+ey)/2,-1)
			else:
				board.set((sx+ex)/2,sy,-1)
			board.set(ex,ey,value)

	def findMove( self, board):
		d = self.depth
		import state
		s = state.State(deepcopy(board),self.tile)
		move = state.alphabeta(s,d,self.tile)
		return move
		



