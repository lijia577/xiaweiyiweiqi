import board, player, state

def main():
	board = Board()
	black_player = HumanPlayer('black', 1)
	white_player = AIPlayer('white', 2)
	#Dispaly initial board
	board.display()
	#First round, remove tiles
	black_player.makeRemove(board)
	board.display()
	white_player.makeRemove(board)
	board.display()
	#Further rounds are in a loop
	while not (black_player.isWin() or white_player.isWin()):
		black_player.makeMove(board)
		board.display()
		white_player.makeMove(board)
		board.display()
	#Show winner
	if black_player.isWin():
		print "Black player wins"
	else:
		print "White player wins"
	



if __name__ == '__main__':
	main()