import state,player,board

b = board.Board()
for i in range(1,9):
	for j in range(1,9):
		b.set(i,j,-1)

b.set(2,4,0)
b.set(2,5,1)
b.set(3,4,1)
b.set(3,5,0)
b.set(3,6,1)

b.display()

s = state.State(b,1,1)

state.minimax(s,3,1)
