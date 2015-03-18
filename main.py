import board, player

def main():
	myBoard = board.Board()
	black_player = player.AIPlayer('black', 1,2)
	white_player = player.AIPlayer('white', 0,3)

	#Dispaly initial board
	myBoard.display()
	#First round, remove tiles
	black_player.makeRemove(myBoard)
	
	myBoard.display()
	white_player.makeRemove(myBoard)
	myBoard.display()
	#Further rounds are in a loop
	while not (black_player.isWin(myBoard) or white_player.isWin(myBoard)):
	 	black_player.makeMove(myBoard)
	 	myBoard.display()
	 	white_player.makeMove(myBoard)
	 	myBoard.display()
	#Show winner
	if black_player.isWin(myBoard):
	 	print "Black player wins"
	else:
	 	print "White player wins"
	



if __name__ == '__main__':
	main()
