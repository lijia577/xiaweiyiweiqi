
class Board():

	def __init__(self):
		#0 for nothing, 1 for x, 0 for o
		row_odd = [0,1,0,1,0,1,0,1]
		row_eve = [1,0,1,0,1,0,1,0]
		self.board_coor = []
		for i in range(8):
			curr_row = row_odd
			if i%2 != 0:
				curr_row = row_eve
			self.board_coor.append(curr_row[:])

	def get(self, x, y):
		# Return number -99 if the x,y is not valid.
		if(x>8 or x<1 or y>8 or y<1):
			return -99
		return self.board_coor[x-1][y-1]

	def set(self, x, y, value):
		if value not in[1,-1,0]:
			print "the board can ONLY be set to 'X', 'O' or '.' "
			return 
		self.board_coor[x-1][y-1] = value

	def display(self):
		mapping  = {0:'O', 1:'X', -1:'.'}
		print "\t1 2 3 4 5 6 7 8\n"
		for i in range(8):
			rep = [mapping[tile] for tile in self.board_coor[7-i]]
			rep = " ".join(rep)
			print 8-i, "\t", rep
		print ""
		
	def checkMovesLeft(self, tile):
		#
		# This functions returns all kinds of one-step moves possible for the given tile.
		# We may want to change it and return number of movable tiles on the board.
		# This function is used in static evaluation function, which affects alphabeta.
		#
		# if the tile next to me is opponent and next next to me is empty,
		# then this tile is movable
		#
		me = tile
		opponent = (tile+1)%2
		movable = 0
		for i in range(8):
			for j in range(8):
				curr = self.board_coor[i][j]
				#check if this is my tile
				if not curr == me:
					continue
				#otherwise, check 4 directions
				movable += self.checkPosition(opponent, (i-1, j), (i-2, j))
				movable += self.checkPosition(opponent, (i+1, j), (i+2, j))
				movable += self.checkPosition(opponent, (i, j-1), (i, j-2))
				movable += self.checkPosition(opponent, (i, j+1), (i, j+2))
		return movable

	def checkPosition(self, opponent, oppo_coor, next_coor):
		# Helper function for checkMovesLeft
		(x1, y1) = oppo_coor
		(x2, y2) = next_coor
		if x1<0 or x2<0 or y1<0 or y2<0 \
		or x1>7 or x2>7 or y1>7 or y2>7:
			return 0
		if not self.board_coor[x1][y1]==opponent \
		or not self.board_coor[x2][y2]==-1:
			return 0
		return 1
	
	



def main():
	board = Board()
	board.display()

if __name__ == '__main__':
	main()






import board, player

def main():

	fw = open("./AI_v_Random_results.txt", "a")
	num_iter = 20 #CHANGE THIS NUMBER TO CHANGE NUMBER OF ITERATIONS
	fw.write("#round, winner, #Black, #White\n")
	for i in range(num_iter):
		result = ""+str(i+1)+","
		myBoard = board.Board()
		black_player = player.RandomPlayer('black', 1,2)
		white_player = player.AIPlayer('white', 0,3)

		#Dispaly initial board
		myBoard.display()
		#First round, remove tiles
		black_player.makeRemove(myBoard)
		myBoard.display()
		white_player.makeRemove(myBoard)
		myBoard.display()
		#Further rounds are in a loop

		while True:
			black_player.makeMove(myBoard)
			myBoard.display()
			if black_player.isWin(myBoard):
		 		print "Black player wins"
		 		break
		 	white_player.makeMove(myBoard)
		 	myBoard.display()
		 	if white_player.isWin(myBoard):
		 		print "White player wins"
		 		break
		if black_player.isWin(myBoard):
			result += "Black,"
		else:
			result += "White,"


		result += str(checkPieces(1, myBoard))+","+str(checkPieces(0, myBoard))+"\n"
	 	fw.write(result);
	
def checkPieces(tile, myboard):
	num = 0
	for i in range(1,9):
		for j in range(1,9):
			if myboard.get(i,j) == tile:
				num = num+1
	return num


if __name__ == '__main__':
	main()
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


import sys
import board   
from copy import deepcopy
import player
import random


class State:
	def __init__(self, board, tile,player, parent=None, action = None):
		self.board = board
		self.parent = parent
		self.kids = [] 
		self.tile = tile # indicates who is playing in this state
		self.action = action
		self.player = player # this player is not changing
	
	def isTerminal(self):
		# this state is terminal if no moves possible for the current tile. 
		return self.board.checkMovesLeft(self.tile)==0

	# input: start crd, output, a list of possible moves starting from this
	def getMoveList(self,startCrd):
		if(self.board.get(*startCrd)!=self.tile):
			print 'Error in getToCoordinates in State class. tile mismatch'
			return None
		#Given a fromCoordinates, return a list of all possible toCoordinates
		res = []
		self.getMoveHelper(startCrd, res, [], [])
		return res[1:]
	
	def getMoveHelper(self, crd, res, path, visited):
		path.append(crd)
		res.append(path)
		
		children = []
		visited.append(crd)
		x,y = crd 
		op = (self.tile+1)%2
		if(self.board.get(x+1,y)==op and self.board.get(x+2,y)==-1 and not((x+2,y)in visited)):
			children.append((x+2,y))
		if(self.board.get(x-1,y)==op and self.board.get(x-2,y)==-1 and not((x-2,y)in visited)):
			children.append((x-2,y))
		if(self.board.get(x,y-1)==op and self.board.get(x,y-2)==-1 and not((x,y-2)in visited)):
			children.append((x,y-2))
		if(self.board.get(x,y+1)==op and self.board.get(x,y+2)==-1 and not((x,y+2)in visited)):
			children.append((x,y+2))
		
		if(len(children)==0):
			return 
		
		for c in children:
			self.getMoveHelper(c,res,path[:],visited)
	
	def getPossibleMoves(self):
		#for the current state, given self.tile. Figure out what moves can be made. Returns a list of (fromCoordinates, toCoordinates).
		res = []
		# color can be determined using self.tile 
		# first, construct a list of movable tiles
		for x in range(1,9):
			for y in range(1,9):
				tile = self.board.get(x,y)			
				#check if the color is right. 
				if(tile == self.tile):
					res.extend(self.getMoveList((x,y)))
		return res
			
	def executeMove(self,board, move):
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
	
	# generate successors 
	def genSucc(self):
		######### IMPLEMENT THIS ##########
		moves = self.getPossibleMoves()
		random.shuffle(moves)
		
		for move in moves:
			newBoard = deepcopy(self.board)
			# execute moves on a deepcoy of this.board
			self.executeMove(newBoard,move) 
			op = (self.tile+1)%2 
			# self is the parent of childNode.
			childNode = State(newBoard,op,self.player, self,move) 
			self.kids.append(childNode)

	# The current static evalution function how many kind of one step move can the black tile make. 
	# It is DIFFERENT from NUMBER of ALL POSSIBLE MOVES currently !
	def staticEval(self, rootTile):
		num1 = self.board.checkMovesLeft(rootTile)
		op = (rootTile+1)%2
		num2 = self.board.checkMovesLeft(op)
		if(num1==0 or num2==0):
			if(self.tile == rootTile):
				# rootTile loses
				#print 'Root Lose'
				return -sys.maxint-1
			else:
				#print 'Root wins'
				return sys.maxint
		else:
			return num1 - num2 
			

def minimax(state, depth, rootTile):
	if(depth ==0):
		print "alphabeta on depth 0 is meaningless. Error"
		return None

	# parameter : the last key is node list. 	
	pm = {'inf':sys.maxint, '-inf':-sys.maxint-1,'cut':0, 'eval':0, 'nl':[]}
	
	res = minimaxhelper(state, True, depth, pm, rootTile)
	
	#book keeping staff: 
	print 'number of cutoffs in pruning: ', pm['cut']
	print 'number of static evaluations: ', pm['eval']
	print 'The average branching factor: ', sum(pm['nl'])/len(pm['nl'])
	
	print 'The Node you are searching for have evaluation score: ', res[0]
	#return res[1]	
	result = getExeNode(res[1])	
	return result.action
	
def minimaxhelper(state,maxFlag, depth, pm, rootTile):
	#generate successors of this state
	state.genSucc()
	pm['nl'].append(len(state.kids))
	if(state.isTerminal()==True or depth==0):
		pm['eval'] +=1 
		return state.staticEval(rootTile), state

	tmp = None

	if maxFlag:
		v = pm['-inf']
		for kid in state.kids:
			# t is tuple containing evaluationScore, state
			t = abhelper(kid, False, depth-1, pm, rootTile)
			v = max(v,t[0])
			if v == t[0]:
				#tmp stores the state with max evaluation score among kdis
				tmp = t[1]
		return v,tmp
	else:
		v = pm['inf']
		for kid in state.kids:
			t = abhelper(kid, True, depth-1, pm, rootTile)
			v = min(v, t[0])
			if v == t[0]:
				tmp = t[1]
		return v,tmp
				
	
def alphabeta(state, depth, rootTile):
	if(depth ==0):
		print "alphabeta on depth 0 is meaningless. Error"
		return None

	# parameter : the last key is node list. 	
	pm = {'inf':sys.maxint, '-inf':-sys.maxint-1,'cut':0, 'eval':0, 'nl':[]}
	
	res = abhelper(state, pm['-inf'], pm['inf'], True, depth, pm, rootTile)
	
	#book keeping staff: 
	print 'number of cutoffs in pruning: ', pm['cut']
	print 'number of static evaluations: ', pm['eval']
	print 'The average branching factor: ', sum(pm['nl'])/len(pm['nl'])
	
	print 'The Node you are searching for have evaluation score: ', res[0]
	#return res[1]	
	result = getExeNode(res[1])	
	return result.action
	
def abhelper(state, a, b, maxFlag, depth, pm, rootTile):
	#generate successors of this state
	state.genSucc()
	pm['nl'].append(len(state.kids))
	if(state.isTerminal()==True or depth==0):
		pm['eval'] +=1 
		return state.staticEval(rootTile), state

	tmp = None

	if maxFlag:
		v = pm['-inf']
		for kid in state.kids:
			# t is tuple containing evaluationScore, state
			t = abhelper(kid, a, b, False, depth-1, pm, rootTile)
			v = max(v,t[0])
			a = max(v,a)
			if v == t[0]:
				#tmp stores the state with max evaluation score among kdis
				tmp = t[1]
			if b<=a:
				pm['cut'] += 1 
				break
		return v,tmp
	else:
		v = pm['inf']
		for kid in state.kids:
			t = abhelper(kid, a, b, True, depth-1, pm, rootTile)
			v = min(v, t[0])
			b = min(v,b)
			if v == t[0]:
				tmp = t[1]
			if b<=a:
				pm['cut'] += 1
				break
		return v,tmp
				

def getExeNode(m):
	#
	# A helper function to trace node to a node close to root. 
	#
	n = m
	while(n.parent.parent!=None):	
		n = n.parent
	return n
	

