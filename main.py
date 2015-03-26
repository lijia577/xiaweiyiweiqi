import board, player

def main():
	#fw = open("./AI_v_Random_results.txt", "a")
	num_iter = 1 #CHANGE THIS NUMBER TO CHANGE NUMBER OF ITERATIONS
	#fw.write("#round, winner, #Black, #White\n")
	for i in range(num_iter):
		result = ""+str(i+1)+","
		myBoard = board.Board()
		black_player = player.RandomPlayer('black', 1,2)
		white_player = player.AIPlayer('white', 0,3)

		#Dispaly initial board
		myBoard.display()
		#First round, remove tiles
		black_player.makeRemove(myBoard)
		myBoard.display()
		white_player.makeRemove(myBoard)
		myBoard.display()
		#Further rounds are in a loop

		while True:
			black_player.makeMove(myBoard)
			myBoard.display()
			if black_player.isWin(myBoard):
				print "Black player wins"
				break
			white_player.makeMove(myBoard)
			myBoard.display()
			if white_player.isWin(myBoard):
				print "White player wins"
				break
		if black_player.isWin(myBoard):
			result += "Black,"
		else:
			result += "White,"

		result += str(checkPieces(1, myBoard))+","+str(checkPieces(0, myBoard))+"\n"
		#fw.write(result);
	
def checkPieces(tile, myboard):
	num = 0
	for i in range(1,9):
		for j in range(1,9):
			if myboard.get(i,j) == tile:
				num = num+1
	return num


if __name__ == '__main__':
	main()
