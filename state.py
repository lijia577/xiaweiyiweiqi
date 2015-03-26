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
		#print 'rootTile is', rootTile
		num1 = self.board.checkMovesLeft(rootTile)
		op = (rootTile+1)%2
		num2 = self.board.checkMovesLeft(op)
		#print 'rootTile num', num1, 'the other', num2
		if(rootTile==self.tile): #AI playing
			if(num1==0):
				return -sys.maxint-1
		else:
			if(num2==0):
				return sys.maxint	
		return num1 - num2 
			

def minimax(state, depth, rootTile):
	if(depth ==0):
		print "alphabeta on depth 0 is meaningless. Error"
		return None

	# parameter : the last key is node list. 	
	pm = {'inf':sys.maxint, '-inf':-sys.maxint-1,'cut':0, 'eval':0, 'nl':[]}
	
	res = minimaxhelper(state, True, depth, pm, rootTile)
	pm['nl']=filter(lambda a: a != 0, pm['nl'])
	#print 'kid length list', pm['nl']
	avbf = sum(pm['nl'])/len(pm['nl'])
	#book keeping staff: 
	print 'number of cutoffs in pruning: ', pm['cut']
	print 'number of static evaluations: ', pm['eval']
	print 'The average branching factor: ', avbf
	
	print 'The Node you are searching for have evaluation score: ', res[0]
	#return res[1]	
	f = open("./minimax_depth5.txt","a")
	analysis = str(pm['cut'])+","+str(pm['eval'])+","+str(avbf)+"\n"
	f.write(analysis)
	f.close()
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
			t = minimaxhelper(kid, False, depth-1, pm, rootTile)
			v = max(v,t[0])
			if v == t[0]:
				#tmp stores the state with max evaluation score among kdis
				tmp = t[1]
		return v,tmp
	else:
		v = pm['inf']
		for kid in state.kids:
			t = minimaxhelper(kid, True, depth-1, pm, rootTile)
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
	pm['nl']=filter(lambda a: a != 0, pm['nl'])
	
	avbf = sum(pm['nl'])/len(pm['nl'])
	#book keeping staff: 
	print 'number of cutoffs in pruning: ', pm['cut']
	print 'number of static evaluations: ', pm['eval']
	print 'The average branching factor: ', avbf
	
	print 'The Node you are searching for have evaluation score: ', res[0]
	f = open("~/Desktop/temp_result.txt","a")
	analysis = str(pm['cut'])+","+str(pm['eval'])+","+str(avbf)+"\n"
	f.write(analysis)
	f.close()
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
	

