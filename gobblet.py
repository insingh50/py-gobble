# Inderpreet Singh
# All the work herein is mine
import random
import copy
##from graphics import *

# gobblePiece
class gP:
    # sizes vary from 1 to 4, 1 being the smallest
    onBoard = False
    def __init__(self, color, size):
        self.color = color
        self.size = size
    def __str__(self):
        return self.color + str(self.size)
    def __repr__(self):
        return self.color + str(self.size)
    def __eq__(self, other):
        return self.color == other.color and self.size == other.size
    def __lt__(self, other):
        return self.size < other.size

# state = board
global currentState
##global hypotheticalState1
##global hypotheticalState2

class gobbleBoard:
    def __init__(self, p1C, p2C):
        self.p1color = p1C
        self.p2color = p2C
        self.rCanMove = True
        self.board = {}
        self.winningColor = ''
        self.previousStates = []
        self.hypotheticalState1 = None
        for row in range(1,5):
            for col in range(1,5):
                self.board[(row,col)] = []
        self.coords = sorted(self.board)
        self.p1Piecesoff = {
            'stack1':[gP(p1C,4),gP(p1C,3),gP(p1C,2),gP(p1C,1)],
            'stack2':[gP(p1C,4),gP(p1C,3),gP(p1C,2),gP(p1C,1)],
            'stack3':[gP(p1C,4),gP(p1C,3),gP(p1C,2),gP(p1C,1)]
            }
            
        self.p2Piecesoff = {
            'stack1':[gP(p2C,4),gP(p2C,3),gP(p2C,2),gP(p2C,1)],
            'stack2':[gP(p2C,4),gP(p2C,3),gP(p2C,2),gP(p2C,1)],
            'stack3':[gP(p2C,4),gP(p2C,3),gP(p2C,2),gP(p2C,1)]
            }

    def __eq__(self, other):
        return self.board == other.board

    def __getitem__(self, key):
        return self.board[key]

    def __str__(self):
        string = "\n"
        for row in range(1,5):
            for col in range(1,5):
                string += str((row,col)) + ":" + str(self.board[(row,col)]) + "\t"
            string += "\n\n"
        string += "Player 1(" + self.p1color.upper() + ")".ljust(22) + "Player 2(" + self.p2color.upper() + ")\n"
        for n in range(1,4):
            stackstr = "stack" + str(n)
            string += stackstr + ": " + str(self.p1Piecesoff[stackstr]).ljust(24) \
                      + stackstr + ": " + str(self.p2Piecesoff[stackstr]) + "\n"
        string += "\n"
        return string

    def setVal(self, x, y, player):
        val = ''
        if player == 1:
            val+p1C
        elif player == 2:
            val+p2C
        return val

    def setBoard(self):
        global currentState
        currentState = self
    def setHypothetical(self, state, n):
        if n == 1:
            self.hypotheticalState1 = gobbleBoard(state.p1color, state.p2color)
            state.deepCopy(self.hypotheticalState1)
        elif n == 2:
            self.hypotheticalState2 = gobbleBoard(state.p1color, state.p2color)
            state.deepCopy(self.hypotheticalState2)
        
    def deepCopy(self, other):
        other.board = copy.deepcopy(self.board)
        other.p1Piecesoff = copy.deepcopy(self.p1Piecesoff)
        other.p2Piecesoff = copy.deepcopy(self.p2Piecesoff)
        other.previousStates = copy.deepcopy(self.previousStates)
    
    def draw(self):
        return self in self.previousStates

    def checkrows(self, color):
        for row in range(1,5):
            if self[(row,1)] != [] and self[(row,2)] != [] and\
               self[(row,3)] != [] and self[(row,4)] != []:
                if self[(row,1)][0].color == color and self[(row,2)][0].color == color and\
                   self[(row,3)][0].color == color and self[(row,4)][0].color == color:
                    self.winningColor = color
                    return True
        return False

    def checkcols(self, color):
        for col in range(1,5):
            if self[(1,col)] != [] and self[(2,col)] != [] and\
               self[(3,col)] != [] and self[(4,col)] != []:
                if self[(1,col)][0].color == color and self[(2,col)][0].color == color and\
                   self[(3,col)][0].color == color and self[(4,col)][0].color == color:
                    self.winningColor = color
                    return True
        return False

    def checkdiagonals(self, color):
        if (self[(1,1)] != [] and self[(2,2)] != [] and\
           self[(3,3)] != [] and self[(4,4)] != []):
            if (self[(1,1)][0].color == color and self[(2,2)][0].color == color and\
                self[(3,3)][0].color == color and self[(4,4)][0].color == color):
                self.winningColor = color
                return True
        if (self[(1,4)] != [] and self[(2,3)] != [] and
            self[(3,2)] != [] and self[(4,1)] != []):
            if (self[(1,4)][0].color == color and self[(2,3)][0].color == color and\
                self[(3,2)][0].color == color and self[(4,1)][0].color == color):
                self.winningColor = color
                return True
        else:
            return False

    def win(self, color):
        s = self
        c = color
        return s.checkrows(c) or s.checkcols(c) or s.checkdiagonals(c)

    def obtainFromStack(self, player, stack):
        if player == 1:
            p1Stack = self.p1Piecesoff[stack]
            piece = p1Stack[0]
            return piece
        elif player == 2:
            p2Stack = self.p2Piecesoff[stack]
            piece = p2Stack[0]
            return piece
    def obtainFromBoard(self, pos):
        piece = self[pos][0]
        return piece
    def removeFrom(self, player, fro, froType):
        if froType == 'stack':
            if player == 1:
                p1Stack = self.p1Piecesoff[fro]
                piece = p1Stack[0]
                p1Stack.remove(piece)
            elif player == 2:
                p2Stack = self.p2Piecesoff[fro]
                piece = p2Stack[0]
                p2Stack.remove(piece)
            # print("removing from stack now")
        elif froType == 'board':
            piece = self[fro][0]
            self[fro].remove(piece)
            
    def canMove(self, toPos):
        return self[toPos] == []
    
    def canGobble(self, toPos, piece):
        return (self[toPos][0] < piece) and piece.onBoard

    ##def status(self, pos, piece):
    ##    if self[pos] == None:
    ##        return 1             # 1 means position is empty
    ##    elif self[pos] < piece:
    ##        return 2             # 2 means position is able to be gobbled
    ##    else:
    ##        return 0    

    def move(self, player, froPos, toPos):
        #if self[toPos] == []:
        if 'stack' in froPos:
            piece = self.obtainFromStack(player, froPos)
            froType = 'stack'
        else:
            piece = self.obtainFromBoard(froPos)
            froType = 'board'
        if not self.canMove(toPos):
            if self.canGobble(toPos, piece):
                self.removeFrom(player, froPos, froType)
                self[toPos].insert(0,piece)
                piece.onBoard = True
                self.setBoard()
            else:
                newToPos = eval(input("Can't place gobblet there, choose a different place to put it: "))
                self.move(player, froPos, newToPos)
        elif self.canMove(toPos):
                self.removeFrom(player, froPos, froType)
                self[toPos].insert(0,piece)
                piece.onBoard = True
                self.setBoard()
        else:
            newToPos = eval(input("Can't place gobblet there, choose a different place to put it: "))
            self.move(player, froPos, newToPos)
            
    def doMoveh1(self, player):
        froPos = input("Player " + str(player) + ": From which stack would you like to move a gobblet? (stack1, stack2, or stack3) ")
        toPos = eval(input("Where would you like to put it? (x,y) "))
        self.previousStates.append(self)
        nextState = gobbleBoard(self.p1color, self.p2color)
        self.deepCopy(nextState)
        nextState.move(player, froPos, toPos)
        print(currentState)

    def doMoveh2(self, player):
        froPos = input("Player " + str(player) + ": Please select a gobblet to move (specify stack or board coordinates) ")
        if ',' in froPos:
            froPos = eval(froPos)
        toPos = eval(input("Where would you like to put it? "))
        self.previousStates.append(self)
        nextState = gobbleBoard(self.p1color, self.p2color)
        self.deepCopy(nextState)
        nextState.move(player, froPos, toPos)
        print(currentState)

    def doMover2(self, player, froPos, toPos, n):
        self.previousStates.append(self)
        nextState = gobbleBoard(self.p1color, self.p2color)
        self.deepCopy(nextState)
        #if nextState[toPos] == []:
        if 'stack' in froPos:
            piece = nextState.obtainFromStack(player, froPos)
            froType = 'stack'
        else:
            piece = nextState.obtainFromBoard(froPos)
            froType = 'board'
        if not self.canMove(toPos):
            if nextState.canGobble(toPos, piece):
                nextState.removeFrom(player, froPos, froType)
                nextState[toPos].insert(0,piece)
                piece.onBoard = True
                nextState.setBoard()
        elif self.canMove(toPos):
            nextState.removeFrom(player, froPos, froType)
            nextState[toPos].insert(0,piece)
            piece.onBoard = True
            if n == 1:
                nextState.setBoard()
                print(currentState)
            elif n == 2:
                nextState.deepCopy(self)
##            elif n == 3:
##              nextState.setHypothetical(2)

    def getAllPossibleMoves(player):
        pass
        

def checkVictoryh(state):
    if state.win('B'):
        print(currentState)
        print("Black wins!")
        input()
        quit()
    elif state.win('W'):
        print(currentState)
        print("White wins!")
        input()
        quit()
    elif state.draw():
        print("Draw!")
        input()
        quit()
def checkVictoryr(state):
    if state.win('B'):
        if state.p1color == 'B':
            return 1
        else: return 2
    elif state.win('W'):
        if state.p1color == 'W':
            return 1
        else: return 2
    elif state.draw():
        return 0

class AImove:
    def __init__(self):
        self.fro = ()
        self.to = ()
        self.score = 0

class AI:
    def __init__(self, aiPlayer):
        self.aiPlayer = aiPlayer
        if aiPlayer == 1:
            self.humanPlayer = 2
        else: self.humanPlayer = 1

    def performMove(self, state, depth):
        bestMove = self.getBestMove(state, self.aiPlayer, depth)
        print(bestMove.fro)
        state.doMover2(self.aiPlayer, bestMove.fro, bestMove.to, 1)
        
    
    def getBestMove(self, state, player, depth):       #self is AI object, state is a gobbleBoar
                                                #player is a string representing Color
##        state.setHypothetical(state, 1)
##        hypo = state.hypotheticalState1
##        originalState = gobbleBoard(state.p1color, state.p2color)
##        state.deepCopy(originalState)
        #Base case, check for end state
        rv = checkVictoryr(state)
        if rv == self.aiPlayer:
##            move.score = 10
            return 10 - depth
        elif rv == self.humanPlayer:
##            move.score = -10
            return depth - 10
        elif rv == 0 or depth < 1:
##            move.score = 0
            return 0
        
        
        
        moves = []
        
        #(x1,y1) is from coordinate, (x2,y2) is to coordinate
        print(state)
        for y1 in range(1,5):
            for x1 in range(1,5):
                if state[(x1,y1)] != [] and state[(x1,y1)][0].color == eval('state.p' + str(player) + 'color'):
                    for y2 in range(1,5):
                        i = 0
                        for x2 in range(1,5):
##                            print('number ' + str(i))
##                            print((x1,y1))
##                            print((x2,y2)) 
                            if state[(x2,y2)] == [] or state[(x2,y2)][0] < state[(x1,y1)][0]:
                                print((x1,y1))
                                print((x2,y2)) 
##                                if i < 2 and eval('state.p' + str(player) + 'PiecesOff[stack' + str(i+1) + ']') != []:
##                                    froPos = 'stack' + str(0+i)
##                                    toPos = (x2,y2)
##                                    move.fro = froPos
##                                    move.to = toPos
##                                    state.doMover2(player, froPos, toPos, 2)
##                                    if player == self.aiPlayer:
##                                        move.score = getBestMove(state, self.humanPlayer).score
##                                    else: move.score = getBestMove(state, self.aiPlayer)
##                                else:
                                move = AImove()
                                froPos = (x1,y1)
                                toPos = (x2,y2)
                                move.fro = froPos
                                move.to = toPos
                                state.doMover2(player, froPos, toPos, 2)
##                                print(state.hypotheticalState1)
                                if player == self.aiPlayer:
                                    move.score = self.getBestMove(state, self.humanPlayer, depth-1)
                                else:
                                    move.score = self.getBestMove(state, self.aiPlayer, depth-1)
                                moves.append(move)
                                #reverse the move made
                                state.doMover2(player, toPos, froPos, 2)
                                i+=1
        bestMove = 0
        if player == self.aiPlayer:
            bestScore = -10000000
            for i in range(0, len(moves)):
                if moves[i].score > bestScore:
                    bestMove = i
                    bestScore = moves[i].score
                i+=1
        else:
            bestScore = 10000000
            for i in range(0, len(moves)):
                if moves[i].score < bestScore:
                    bestMove = i
                    bestScore = moves[i].score
                i+=1
        return moves[bestMove]
            


                                
                                



########################### GAME START #################################
#def main():
#HUMAN VS HUMAN
prompt1 = input('Select a game mode (h2, hr, rh, r2): ')
if prompt1 == 'h2':
    p1Color = input("Player 1: choose your color (black or white) ").upper()
    if 'B' in p1Color:
        p1Color = "B"
        p2Color = "W"
    else:
        p1Color = "W"
        p2Color = "B"

    myBoard = gobbleBoard(p1Color, p2Color)
    myBoard.setBoard()

    print(currentState)

    #Player 1's first move
    currentState.doMoveh1(1)

    #Player 2's first move
    currentState.doMoveh1(2)

    while True:
        currentState.doMoveh2(1)
        checkVictoryh(currentState)
        currentState.doMoveh2(2)
        checkVictoryh(currentState)

    print(currentState)

#ROBOT VS HUMAN / ROBOT IS PLAYER 1
elif prompt1 == 'rh':
    aicolor = 'bw'[random.randint(1, 2)].upper()
    AI = AI(1)
    hcolor = AI.humanPlayer
    print("Robot is " + aicolor + ".\n")

    myBoard = gobbleBoard(aicolor, hcolor)
    myBoard.setBoard()

##    doMoveh1(currentState, 2)
    doMoveh2(currentState, 2)

    print(currentState)

    #robots first move







#HUMAN VS ROBOT / HUMAN IS PLAYER 1
elif prompt1 == 'hr':
    hcolor = input("Pick your color, human: ").upper()
    if 'B' in hcolor:
        hcolor = 'B'
        aicolor = 'W'
    else:
        hcolor = 'W'
        aicolor = 'B'
    AI = AI(2)
    depth = int(input('Select a depth amount: '))

    board = {(1, 1): [gP('B',4)], (1, 2): [], (1, 3): [gP('B',4)], (1, 4): [], (2, 1): [gP('W',3)], (2, 2): [], (2, 3): [],\
             (2, 4): [], (3, 1): [gP('B',3)], (3, 2): [], (3, 3): [], (3, 4): [], (4, 1): [gP('W',4)], (4, 2): [],\
             (4, 3): [gP('W',4)], (4, 4): [gP('W',3)]}
    
    myBoard = gobbleBoard(hcolor, aicolor)
    myBoard.board = board
    myBoard.setHypothetical(myBoard, 1)
    hypo = myBoard.hypotheticalState1
    myBoard.setBoard()

    print(currentState)

    while(True):
        currentState.doMoveh2(1)
        checkVictoryh(currentState)
        AI.performMove(currentState, depth)
        checkVictoryh(currentState)

    print(currentState)

    #robots first move











#main()























