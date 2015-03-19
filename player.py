import board, random
from copy import deepcopy
from ast import literal_eval

class Player():
	def __init__(self, color, tile):
		#color: black(X) or white(O), NOT SURE IF WE NEED IT
		#tile: 1(X) or 0(O) 
		self.color = color
		self.tile = tile
	def makeRemove(self, board):
		pass
	def makeMove(self, board):
	 	pass
	def findRemove(self, board):
	 	return []#override
	def findMove(self, board):
	 	return []#override
	def isWin(self, board):
		# You win when your opponent has nothing to move
		opponent = (self.tile+1)%2
		return board.checkMovesLeft(opponent) == 0

class HumanPlayer(Player):
	
	def getInput(self, msg = None, remove = False):
		re = []
		
		#message stuff
		if remove:
			print "In remove stage, you can only input one tuple"
		elif msg is not None:
			print "Enter n at any time if you wish to end your round!"
			print msg
		

		#loop
		while True:

			#take raw input
			raw = raw_input("please enter the move you with to make(or n to end your round):  ")

			#exit condition
			if 'n' in raw:
				break

			#format string
			temp = raw.strip('()').replace(' ','').split(',')
			
			print temp
			#illegal input
			if len(temp) != 2:
				#msg
				print "Illegal input. You can only input a tuple of two integers seperated by ',' !"
				continue
			try:
				cargo = int(temp[0]), int(temp[1])	
				re.append(cargo)
				#remove stage
				if remove:
					print "END OF REMOVE ROUND"
					print "####################################################"
					return re
			except:
				print "Illegal characters in input, only digits and ',' is allowed!"
				print "Try again!"
		return re

	def makeRemove(self, board):
		print "Making remove..."
		#make a remove at selected location

		while True:
			#ask user for coordinates to remove
			print "Enter the Position (x,y) You Want to Remove."
			
			#take input			
			moves = self.getInput(remove = True)

			#format input
			x = moves[0][0]
			y = moves[0][1]

			#check if valid
			if self.tile == 1: #black tile
				if (x,y) == (8,1) or (x,y) == (1,8) \
				or (x,y) == (4,5) or (x,y) == (5,4):
					break
			else: 
				#white tile, needs to check adjacent tiles
				if (((x+1, y) == (8,1) or (x,y-1) == (8,1)) and board.get(8,1)==-1) \
				or (((x, y-1) == (1,8) or (x+1,y) == (1,8)) and board.get(1,8)==-1) \
				or (((x, y) == (4,4) or (x,y) == (5,5)) and (board.get(4,5) == -1 or board.get(5,4)==-1)):
					break

			#msg for invalid pos
			print "Invalid position. Try again."

		#finalize move
		board.set(x, y, -1)
		return True
	
	def makeMove(self,board):
		#ask user to follow instructions
		while True:

			moves = self.getInput("Enter your move following instructions!")
			if len(moves) < 2 :
				continue

			opponent = (self.tile+1)%2
			success = 1
			

			for i in range(len(moves)-1):
				(x1,y1) = moves[i]
				(x2,y2) = moves[i+1]
				if (i == 0 and board.get(x1, y1) != self.tile) or \
					(i != 0 and board.get(x1, y1) != -1) or \
					board.get(x2,y2) != -1 or \
					(x1==x2 and abs(y1-y2)!=2) or \
					(y1==y2 and abs(x1-x2)!=2) or \
					(x1==x2 and board.get(x1,(y1+y2)/2) != opponent) or \
					(y1==y2 and board.get((x1+x2)/2, y1) != opponent):
						success = 0
						break
			if success:
				list_of_moves = moves
				for i in range(len(list_of_moves)-1):
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
				print "END OF YOUR ROUND!"
				print "###################################################"
				return True	


			else:
				print "Your moves can't be made, double check and try again"
				print "###################################################"
	



class AIPlayer(Player):
	def __init__(self, color, tile,depth):
		self.color = color
		self.depth = depth
		self.tile = tile


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
		for i in range(len(list_of_moves)-1):
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
		s = state.State(deepcopy(board),self.tile,self)
		move = state.alphabeta(s,d,self.tile)
		return move

class RandomPlayer(AIPlayer):
	def findMove(self, board):
		import state
		s = state.State(deepcopy(board), self.tile, self)
		movable = []
		me = self.tile
		opponent = (me+1)%2


		for i in range(8):
				for j in range(8):
					if board.get(i+1,j+1) != me:
						continue
					if board.checkPosition(opponent, (i-1, j), (i-2, j)) or\
					board.checkPosition(opponent, (i+1, j), (i+2, j)) or\
					board.checkPosition(opponent, (i, j-1), (i, j-2)) or\
					board.checkPosition(opponent, (i, j+1), (i, j+2)) :
						movable.append((i+1,j+1))
		
		random.shuffle(movable)
		list_of_moves = s.getMoveList(movable[0])
		random.shuffle(list_of_moves)
		return list_of_moves[0] #list of coors


