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

s = state.State(b,1)

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
print s.getPossibleMoves()
"""
print "Start: test get possible moves"
res = s.getPossibleMoves()
print 'all possible moves for black at this point', res
print 'length of all possible moves are 7?  ', len(res)

print 'test executeMove on board b'
#b.display()
#s.executeMove(b,(7,5),(5,5))
#b.display()


print 'Next, test genSucc function'
s.genSucc()
print 'len should be 7', len(s.kids)

print 'Check child state 1 ....'
print 'before'
s.board.display()

k1 = s.kids[0]
print 'after action', k1.action
k1.board.display()

print 'Check child state 7....'

k2 = s.kids[6]
print 'with action', k2.action
k2.board.display()



print 's tile should be 1', s.tile
print 'k1 tile is ?',k1.tile
print 'k2 tile is ?',k2.tile

k2.genSucc()

k22 = k2.kids[0]
print 'k22 tile is?', k22.tile



print 'checing static evaluation function of s, k1, k2 black is playing '
print s.staticEval(1)
print k1.staticEval(1)
print k2.staticEval(1)

"""


































