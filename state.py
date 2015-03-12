import sys
import board   
from copy import deepcopy
import player


class State:
	def __init__(self, board, tile, parent=None, action = None):
		self.board = board
		self.parent = parent
		self.kids = [] 
		self.tile = tile # indicates who is playing right now.
		self.action = action
	
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
	
	def executeMove(self, board, move):
		x1,y1 = fromCrd
		value = board.get(x1,y1)
		board.set(x1,y1,-1)
		x2,y2 = toCrd
		board.set(x2,y2,value)
		if(x1<1 or x2<1 or y1>8 or y2>8):
			print 'Warning! in executeMove in state class'
	
	
	# generate successors 
	def genSucc(self):
		######### IMPLEMENT THIS ##########
		moves = self.getPossibleMoves()
		
		for move in moves:
			newBoard = deepcopy(self.board)
			# execute moves on a deepcoy of this.board
			self.executeMove(newBoard, *move) 
			op = (self.tile+1)%2 
			# self is the parent of childNode.
			childNode = State(newBoard,op,self,move) 
			self.kids.append(childNode)

	# The current static evalution function how many black tiles ,for exmaple, are MOVABLE. 
	# It is DIFFERENT from NUMBER of ALL POSSIBLE MOVES currently !
	def staticEval(self, rootTile):
		if(self.isTerminal()==True):
			if(self.tile == rootTile):
				# rootTile loses
				return -sys.maxint-1
			else:
				#root tile wins
				return sys.maxint
		else:
			#  WE CARE ABOUT ROOT TILE NOT SELF.TILE
			num1 = self.board.checkMovesLeft(rootTile)
			op = (rootTile+1)%2 
			num2 = self.board.checkMovesLeft(op)
			# moves root tile can make - moves oppenent can make
			print 'num1 is ', num1, 'num2 is ', num2
			return num1 - num2 
			

	@staticmethod
	def alphabeta(state, maxFlag, depth):
		if(depth ==0):
			print "alphabeta on depth 0 is meaningless. Error"
			return None
	
		# parameter : the last key is node list. 	
		pm = {'inf':sys.maxint, '-inf':-sys.maxint-1,'cut':0, 'eval':0, 'nl':[]}
		
		res = abhelper(state, pm['-inf'], pm['inf'], maxFlag, depth, pm, state.tile)
		
		#book keeping staff: 
		print 'number of cutoffs in pruning: ', pm['cut']
		print 'number of static evaluations: ', pm['eval']
		print 'The average branching factor: ', sum(pm['nl'])/len(pm['nl'])
		
		print 'DEBUG the node you are searching for have evaluation score: ', res[0]
		return res[1]	

	@staticmethod
	def abhelpher(state, a, b, maxFlag, depth, pm, rootTile):
		#generate successors of this state
		state.genSucc()
		pm['nl'].append(len(state.kids))
	
		if(state.isTerminal()==True or depth==0):
			pm['eval'] +=1 
			return state.staticEval(root), state

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
				
	@staticmethod	
	def rootToNodeList(n):
		li = []
		while(n.parent!=None):
			li.append(n)
			n = n.parent
		li.append(n)
		li.reverse()
		return li
	

