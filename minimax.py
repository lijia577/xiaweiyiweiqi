import sys

    
class Node:
	def __init__(self, value, parent = None):
		self.value = value
		self.parent = None
		self.kids = []
        
	def isTerminal(self):
		return len(self.kids)==0
            
	
	def printKids(self):
		for x in self.kids:
            		print x.value,
        	print ""

				
		

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
	node = n
	while(node.parent.parent!=None):
		node = node.parent
	return node



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

	res = alphaBeta(a,True, eFoo,10)
	print rootToNodeList(res).value






