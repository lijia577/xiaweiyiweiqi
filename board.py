class Board():
	def __init__(self):
		#0 for nothing, 1 for x, 2 for o
		row_odd = [2,1,2,1,2,1,2,1]
		row_eve = [1,2,1,2,1,2,1,2]
		self.board_coor = []
		for i in range(8):
			curr_row = row_odd
			if i%2 != 0:
				curr_row = row_eve
			self.board_coor.append(curr_row[:])
	def get(self, x, y):
		return self.board_coor[x][y]
	def set(self, x, y, value):
		#check value is in {0, 1, 2}?
		self.board_coor[x][y] = value
	def display(self):
		mapping  = {0:'.', 1:'X', 2:'O'}
		print "\t1 2 3 4 5 6 7 8\n"
		for i in range(8):
			rep = [mapping[tile] for tile in self.board_coor[7-i]]
			rep = " ".join(rep)
			print 8-i, "\t", rep




