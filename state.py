import copy
class State():
	def __init__(self, curr_board, curr_player, parent_state ):
		self.curr_board = curr_board # a board object
		self.curr_player = curr_player # 0(white) or 1(black)
		self.parent_state = parent_state # a state object
	def getSuccessors(self):
		#pesudocode
		#successors = []
		#for item in self.curr_board,
		#	if item == self.curr_player:
		#		get its possible moves, including steps from 1 to n
		#		for each move, make that move on the current board, 
		#		update player, add to successors
		#NOTE: be careful with changing/updating the board, 
		#always gets a deep copy of board, or initialize a new board
		#to get deep copy, import copy and call copy.deepcopy(something)