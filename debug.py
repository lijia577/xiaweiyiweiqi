import board
import player

 

l1 = [-1, 0, -1, 0, 1, 0, -1, 0]
l2 = [-1,-1,-1,-1,0, -1, -1, 1]
l3 = [1, -1, -1, -1, 1, -1, 1, -1]
l4 = [-1, -1, -1, -1, -1, -1, -1, -1]
l5 = [1, 0, -1 ,-1 , -1, 0, -1 , -1]
l6 = [-1, -1, -1, 1, -1, -1, -1, -1]
l7 = [-1, -1, -1, -1, -1, 0, -1 , -1]
l8 = [0, 1, 0, -1, -1, 1, 0, 1]
 
l = []
l.extend(l8)
l.extend(l7)
l.extend(l6)
l.extend(l5)
l.extend(l4)
l.extend(l3)
l.extend(l2)
l.extend(l1)
 

b = board.Board()


i = 0
for x in range(1,9):
	for y in range(1,9):
		b.set(x,y,l[i])
		i+=1

b.display()
import state
from copy import deepcopy
s = state.State(deepcopy(b),1)

print s.isTerminal(), '? false'


s.board.display()
print 'Start test getToCoordinates'

crd1 = (1,6)
l1 = s.getMoveList(crd1)
crd2 = (4,1)
l2 = s.getMoveList(crd2)
print l1
print l2

print 'Test get all possible moves'
testMove =  s.getPossibleMoves()
print testMove

print 'test execute move'
singleMove = testMove[2]


from copy import deepcopy
tb = deepcopy(s.board)
print'before Move'
tb.display()
s.executeMove(tb,singleMove)
print 'after move', singleMove
tb.display()



print '********************'
print 'Test generate sucuessor function'

print 'root board state'
s.board.display()
s.genSucc()
print 'root board should have 7 successor board state' , len(s.kids)

print 'The firld child board state'
s.kids[0].board.display()

s.kids[0].genSucc()
print 'kis 0 has 6 successors', len(s.kids[0].kids)

print 'the successor of kid 0 of s'
s.kids[0].kids[5].board.display()

#print 'The second child board state'
#s.kids[6].board.display()

print 'Testing - Static evalutation'
print 'Testing root state static evaluation'
print s.staticEval(1)
print s.kids[0].staticEval(1)
print s.kids[0].kids[5].staticEval(1)

print s.kids[0].action

print ""
print ""
print '----------'

print 'Testing -alphabeta pruning'
b.display()
move = state.alphabeta(s,True,8,1)
print move
s.executeMove(b,move)
b.display()

move = [(8,8),(6,8),(6,6),(6,4)]
s.executeMove(b,move)
b.display()

newState = state.State(deepcopy(b),1)
move = state.alphabeta(newState,True,8,1)
print move
newState.executeMove(b,move)
b.display()

print 'End of first alphabeta test case.'



l1 = [-1, -1, -1, -1, -1, -1, -1, -1]
l2 = [-1, -1, -1, -1, -1, -1, -1, -1]
l3 = [-1, -1, -1, -1, -1, -1, -1, -1]
l4 = [-1, -1, -1, -1, -1, -1, -1, -1]
l5 = [-1, -1, -1, -1, -1, -1, -1, -1]
l6 = [-1, -1, -1,  1,  0,  1, -1, -1]
l7 = [-1, -1, -1,  0,  1, -1, -1, -1]
l8 = [-1, -1, -1, -1, -1, -1, -1, -1]


l = []
l.extend(l8)
l.extend(l7)
l.extend(l6)
l.extend(l5)
l.extend(l4)
l.extend(l3)
l.extend(l2)
l.extend(l1)

from state import alphabeta
b = board.Board()


i = 0
for x in range(1,9):
	for y in range(1,9):
		b.set(x,y,l[i])
		i+=1

print 'Testing with a different board'
b.display()

s = state.State(deepcopy(b),1)
move = alphabeta(s,True,10,1)
print move 
s.executeMove(b,move)
b.display()
print "user's turn"
move = [(3,5),(1,5)]
s.executeMove(b,move)
b.display()

s = state.State(deepcopy(b),1)
move = alphabeta(s,True,10,1)
print move
s.executeMove(b,move)
b.display()


































