import sys

   

class State:
	import board
	def __init__(self, board, tile, parent=None):
		self.board = board
		self.parent = parent
		self.kids = [] 
		self.tile = tile # indicates who is playing right now.

	def isTerminal(self):
		# this state is terminal if no moves possible for the current tile. 
		return board.checkMovesLeft(self.tile)==0
	
	def getToCoordinates(self,fromCoordinates):
		"""
		Given a fromCoordinates, return a list of all possible toCoordinates
		"""
		#Implementing BFS
		res = []
		visited = set()
		op =(self.tile+1)%2;
		frontier = [fromCoordinates]
		while(len(frontier)>0):
			cur  = frontier.pop(0)
			visited.add(cur)
			
			x,y = cur
		
			if(self.board.get(x+1,y) == op and self.board.get(x+2,y) == -1 and not((x+2,y) in visisted)):
				crd = (x+2, y)
				res.append(crd)
				frontier.append(crd)
			if(self.board.get(x,y+1) == op and self.board.get(x,y+2) == -1 and not((x,y+2)in visited)):
				crd = (x,y+2)
				res.append(crd)
				frontier.append(crd)
			if(self.board.get(x-1,y) == op and  self.board.get(x-2, y) ==-1 and not((x-2,y)in visited)):
				crd = (x-2,y)
				res.append(crd)
				frontier.append(crd)
			if(self.board.get(x,y-1) == op and self.board.get(x,y-2) == -1 and not((x,y-2)in visited)):
				crd = (x, y-2)
				res.append(crd)
				frontier.append(crd)
		return res	
		
	
	def getPossibleMoves(self):
		"""
		for the current state, given self.tile. Figure out what moves can be made. Returns a list of (fromCoordinates, toCoordinates).
		"""	
		res = []
		# color can be determined using self.tile 
		# first, construct a list of movable tiles
		for x in range(8):
			for y in range(8):
				fromCrd = (x,y)
				tile = self.board.get(*fromCrd)
				#check if the color is right. 
				if(tile == self.tile):
					toCrdList = getToCoordinates(tile)
					for toCrd in toCrdList:
						res.append((fromCrd,toCrd))

	# generate successors 
	def genSucc(self):
		from copy import deepcopy
		import player
		######### IMPLEMENT THIS ##########
		moves = self.getPossibleMoves()
		
		for move in moves:
			newBoard = deepcopy(this.board)
			# execute moves on a deepcoy of this.board
			player.makeMove(newBoard, *move) 
			op = (self.tile+1)%2 
			# self is the parent of childNode.
			childNode = State(newBoard,op,self) 
			self.kids.append(childNode)


	def staticEval(self, rootTile):
		import sys
		if(board.checkMovesLeft(self.tile)==0):
			if(self.tile == rootTile):
				# rootTile loses
				return -sys.maxint-1
			else:
				#root tile wins
				return sys.maxint
		else:
			#  WE CARE ABOUT ROOT TILE NOT SELF.TILE
			num1 = len(getPossibleMoves(self.board, rootTile))
			# this can be INEFFICIENT!
			op = (rootTile+1)%2 
			num2 = len(getPossibleMoves(self.board,op)
			# moves root tile can make - moves oppenent can make
			return num1 - num2 
			


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
				
		

# >>> This should return a move that leading to you the optimal track. 
# Ideally, this should return a path leading to THE NODE. 
# returns a node in the tree which optimizes your max-min agenda...
def alphaBeta(node,maximizing,eFoo,depth):
	if(depth == 0):
		print 'calling alpha beta with depth 0 is meaningless!'
		return None
	para = {'inf':sys.maxint, '-inf':-sys.maxint-1,'cut':0, 'eval':0, 'nl':[]}
	res = abpruning(node,para['-inf'], para['inf'], maximizing, eFoo, depth, para)
	return res[1]
	

# here maximizing is a boolean value. 
def abpruning(node, a, b, maximizing, eFoo, depth, para):
	'''
	If we a node has two children whose heuristic are the same, this algorithms return the later child. 
	'''
	if(node.isTerminal() ==True or  depth==0):
		para['eval'] += 1
		return (eFoo(node),node)
	tmp = None
	para['nl'].append(len(node.kids))
	if maximizing:
		v = para['-inf']	
		for kid in node.kids:
			tup = abpruning(kid,a,b,False,eFoo,depth-1,para)
			v = max(v,tup[0]) #value of current node.
			a = max(v,a) # update a if necessary
			if v ==tup[0]: 
				tmp = tup[1] #tmp stores the node with min/max value among kids 
			if b <=a:
				para['cut'] += 1
                		break
		return v,tmp
	else:
		v = para['inf']
		for kid in node.kids:
			tup = abpruning(kid, a, b, True, eFoo, depth-1,para)
			v = min(v,tup[0])
			b = min(v,b)
			if v == tup[0]:
				tmp = tup[1] # tmp stores the node with min value among kids 
			if b<=a:
				para['cut'] += 1
				break
		return v,tmp
                    
#return a list from root to node
def rootToNodeList(n):
	li = []
	while(n.parent!=None):
		li.append(n)
		n = n.parent
	li.append(n)
	li.reverse()
	return li



# return a number that is closest to the number 10  
# >>> eFoo MUST BE A MONOTONIC INCREASING FUNCTION. MEANING, FOR A GOOD NODE, IT RETURNS A HIGHER VALUE.  
def eFoo(node):
	# evaluaion function of a node. Here, we care about whether the value of node is close to 9
	#return sys.maxint-abs(node.value-10);
	return node.value
    

                    
if __name__=="__main__":
	a = Node(0)
	b = Node(1)
	c = Node(2)
	x = Node(3)

	d = Node(16)
	e = Node(4) 
	f = Node(9)

	g = Node(3)	
	h = Node(9)
	
	y = Node(0) 
    
	a.kids.append(b)
	a.kids.append(c)
	a.kids.append(x)
	b.parent = a
	c.parent = a
	x.parent = a

	b.kids.append(d)
	b.kids.append(e)
	b.kids.append(f)
    
	d.parent = b
	e.parent = b
	f.parent = b
	
	c.kids.append(g)	
	c.kids.append(h)

	g.parent =c 
	h.parent = c
	
	x.kids.append(y)
	y.parent = x

	res = alphaBeta(a,True, eFoo,3)
	print rootToNodeList(res)






