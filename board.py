
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
		return self.board_coor[x][y]
	def set(self, x, y, value):
		#check value is in {0, 1, -1}?
		self.board_coor[x][y] = value
	def display(self):
		mapping  = {0:'O', 1:'X', -1:'.'}
		print "\t1 2 3 4 5 6 7 8\n"
		for i in range(8):
			rep = [mapping[tile] for tile in self.board_coor[7-i]]
			rep = " ".join(rep)
			print 8-i, "\t", rep
	def checkMovesLeft(self, tile):
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
		(x1, y1) = oppo_coor
		(x2, y2) = next_coor
		if x1<0 or x2<0 or y1<0 or y2<0 \
		or x1>7 or x2>7 or y1>7 or y2>7:
			return 0
		if not self.board_coor[x1][y1]==opponent \
		or not self.board_coor[x2][y2]==-1:
			return 0
		return 1
	











