import boardPos
playerOne = ""
playerTwo = ""

# Functions
def selectColors():
    print("-" * 75) 
    p1Color = input
    
    while True:
        p1Color = (input("Player 1, please select a color! ('r' for red and 'y' for yellow: ").lower())
        
        if p1Color == 'y' or p1Color == 'r':
            return p1Color
        else:
            print("Please select a valid Connect4 color!")
def printBoard():
     print("--"*8)
     for i in range(6):
        print("|", end = " ")
        for j in range(7):
            print(boardPos.board[j][i], end=" ")

        print("|")
     print("--"*8)
            

def checkConnect4(columnNum, level, player):
    
    connectedDiskCounter = 0
    numConnect4s = 0
    
    # Check vertical
    for i in range(6, 0, -1):
        if boardPos.board[columnNum][i-1] == player:
            connectedDiskCounter +=1
            if connectedDiskCounter == 4:
                numConnect4s +=1
        else:
            connectedDiskCounter = 0
        #print(f"connected pieces: {connectedDiskCounter}")
    
    # Check Horizontal'
    connectedDiskCounter = 0
    for i in range(0,7):
        if boardPos.board[i-1][level] == player:
            connectedDiskCounter +=1
            if connectedDiskCounter == 4:
                numConnect4s +=1
        else:
            connectedDiskCounter = 0 
        #print(f"connected pieces: {connectedDiskCounter}")
    
    for i in range(0,4):
        if (i) == 0 or (i) == 1:
            connectedDiskCounter = 0
            for j in range(6,0,-1):
                    if boardPos.board[6-j+i][j-1] == player:
                        connectedDiskCounter +=1
                        if connectedDiskCounter == 4:
                                numConnect4s +=1
                                
                    else:
                            connectedDiskCounter = 0
        elif i == 2:
            connectedDiskCounter = 0
            for j in range(5,0,-1):
                    if boardPos.board[(5-j)+i][5-(5-j)] == player:
                        connectedDiskCounter +=1
                        if connectedDiskCounter == 4:
                                numConnect4s +=1
                                
                    else:
                            connectedDiskCounter = 0
        elif i == 3:
            connectedDiskCounter = 0
            for j in range(4,0,-1):
                    if boardPos.board[(4-j)+i][5-(4-j)] == player:
                        connectedDiskCounter +=1
                        if connectedDiskCounter == 4:
                                numConnect4s +=1
                                
                    else:
                            connectedDiskCounter = 0
    # Check diagonal right
    for i in range(6,2,-1):
        if (i) == 6 or (i) == 5:
            connectedDiskCounter = 0
            for j in range(6,0,-1):
                    if boardPos.board[i-(6-j)][j-1] == player:
                        connectedDiskCounter +=1
                        if connectedDiskCounter == 4:
                                numConnect4s +=1
                                
                    else:
                            connectedDiskCounter = 0
        elif i == 4:
            connectedDiskCounter = 0
            for j in range(5,0,-1):
                    if boardPos.board[i-(5-j)][5-(5-j)] == player:
                        connectedDiskCounter +=1
                        if connectedDiskCounter == 4:
                                numConnect4s +=1
                                
                    else:
                            connectedDiskCounter = 0
        elif i == 3:
            connectedDiskCounter = 0
            for j in range(4,0,-1):
                    if boardPos.board[i-(4-j)][5-(4-j)] == player:
                        connectedDiskCounter +=1
                        if connectedDiskCounter == 4:
                                numConnect4s +=1
                                
                    else:
                            connectedDiskCounter = 0  
          
          
                
    return numConnect4s        
def gameloop(p1Color,p2Color):
    spacesUsed = []
    rowsUsed = [] # In order for the a to g from spacesUsed
    spaceColor = []
    import boardPos
    currentPlayer = 1
    gameActive = True
    level = 0
    while(gameActive == True):
            correctIn = False 
            playerChoice = int(input(f"Player {currentPlayer}, Where on the board do you wish to drop your piece (1 to 7)?: "))
            if (playerChoice <= 7) and (playerChoice >= 1):
               correctIn = True 
               for item in range(6,0, -1):
                   if (boardPos.board[playerChoice - 1][item-1] == 0) and (item <= 6):
                       boardPos.board[playerChoice - 1][item-1] = currentPlayer
                       level = item-1
                       break
                   elif item <= 1:
                       print("That colunn is filled up!")
                       correctIn = False
            else:
                    print(f"Player {currentPlayer}, please input a valid location!")
            
            
            if correctIn == True:
                printBoard()
                connect4s = checkConnect4(playerChoice-1, level, currentPlayer)
                if connect4s > 0:
                    gameActive == False
                    break
                
                if currentPlayer == 1:
                    currentPlayer = 2
                else:
                    currentPlayer = 1
                
    print(f"Player {currentPlayer} wins with {connect4s} Connect 4's!")

                
                

            

print("Welcome to Connect4!")

playerOne = selectColors()
if (playerOne == "r"):
    playerOne == "Red"
    playerTwo= "Yellow"
   
    print(f"Player 1 is Red | Player 2 is Yellow")


else:
    playerOne = "Yellow"
    playerTwo = "Red"
    print(f"Player 1 is Yellow | Player 2 is Red")

#print("Rules: ", end="")
gameloop(playerOne, playerTwo)

    



