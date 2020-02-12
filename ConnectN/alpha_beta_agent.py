import math
import agent
from heapq import heappush, heappop

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        
        return self.abp(brd, self.max_depth)

    def abp(self, brd, depth):
        inf = float('inf')
        ninf = -float('inf')
        best_move = self.max_value(brd, ninf, inf, depth)
         
        return best_move
        
        
        
#    def max_value(self, brd, alpha, beta, depth):
##        if self.is_end(brd):
##            return float('inf')
#        if depth == 0:    # check if game over
#            return self.heuristic(brd)
#        v = -float('inf')
#        priQ = []
#        for (nb, col) in self.get_successors(brd):
#            heappush(priQ, self.min_value(nb, alpha, beta, depth-1)*-1)
#            
#        while(priQ):
#            v = max(v, heappop(priQ)*-1)  # the best case for us
#            if v >= beta:
#                return v
#            alpha = max(alpha, v) # update alpha
#        return v
    
#    def min_value(self, brd, alpha, beta, depth):
##        if self.is_end(brd):
##            return -float('inf')
#        if depth == 0:    # check if game over
#            return self.heuristic(brd)
#        v = float('inf')
#        priQ = []
#        for (nb, col) in self.get_successors(brd):
#            heappush(priQ, self.max_value(nb, alpha, beta, depth-1))
#            
#        while(priQ):
#            v = min(v, heappop(priQ))  # the best case for us
#            if v <= alpha:
#                return v
#            beta = min(beta, v) # update alpha
#        return v
        
    def max_value(self, brd, alpha, beta, depth):
#        if self.is_end(brd):
#            return float('inf')
        if depth == 0:    # check if game over
            x = self.heuristic(brd)
            return x
        v = -float('inf')
        best_col = 0
        
        for (nb, col) in self.get_successors(brd):
            v = max(v, self.min_value(nb, alpha, beta, depth-1))  
            if v >= beta:
                return v
            
            if v > alpha: # update alpha
                alpha = v
                best_col = col
             
        if depth == self.max_depth:
            return best_col
        else:
            return v
    
    def min_value(self, brd, alpha, beta, depth):
#        if self.is_end(brd):
#            return -float('inf')
        if depth == 0:    # check if game over
            x = self.heuristic(brd)
            return x
        v = float('inf')
    
        for (nb, col) in self.get_successors(brd):
            v = min(v, self.max_value(nb, alpha, beta, depth-1)) 
            if v <= alpha:
                return v
            beta = min(beta, v) # update alpha
        return v
    
#-----------------------------------------------------------------------------        

    def heuristic(self, brd):
        score = 0
        player = self.player
        other = 3-player
        for y in range(brd.h):
            for x in range(brd.w):
                if brd.board[y][x] == player:
                    score +=1
                    if x == 3:
                        score +=2
                    if brd.is_any_line_at(x, y):
                        score += 1000
                    else: 
                        score += self.connectn(brd, x, y, 1, 0, player)
                        score += self.connectn(brd, x, y, 1, 1, player)
                        score += self.connectn(brd, x, y, 1, -1, player)
                        score += self.connectn(brd, x, y, 0, 1, player)
                    score += self.block(brd, x, y, other)
                    
                elif brd.board[y][x] != player and brd.board[y][x] != 0:
                    score -=1
                    if x == 3:
                        score -=2
                    if brd.is_any_line_at(x, y):
                        score -= 1000
                    else: 
                        score -= self.connectn(brd, x, y, 1, 0, other)
                        score -= self.connectn(brd, x, y, 1, 1, other)
                        score -= self.connectn(brd, x, y, 1, -1, other)
                        score -= self.connectn(brd, x, y, 0, 1, other)
        return score
                    

    def block(self, brd, x, y, player):
        score = 0
        if self.is3at(brd, 3, x, y, 1, 0, player):
            score += 16
        if self.is3at(brd, 3, x, y, 1, 1, player):
            score += 16
        if self.is3at(brd, 3, x, y, 1, -1, player):
            score += 16
        if self.is3at(brd, 3, x, y, 0, 1, player):
            score += 16
        return score

    def connectn(self, brd, x, y, dx, dy, player):
        score = 0
        connected = 1
        bonus = 0
        blocked = 0
        column = 0
        for i in range(1, 5):
            if y + i*dy >= brd.h or x +i*dx >= brd.w or y + i*dy < 0:
                blocked = 1
                break
            if brd.board[y+i*dy][x+i*dx] == player and connected >= 1:
                score += (i+1)**2
                connected += 1
            elif brd.board[y+i*dy][x+i*dx] == 0 and connected == 3:
                connected = 0
                bonus = i**2
                score += bonus
                column = x+i*dx
            elif brd.board[y+i*dy][x+i*dx] == 0:
                connected = 0
            elif brd.board[y+i*dy][x+i*dx] == player:
                connected = 0
                blocked = 1

        if y-dy>=0 and y-dy<brd.h and x-dx >=0:
            if brd.board[y-dy][x-dx] == player:
                score += bonus
        return score
        # if blocked == 0 && dx != 0:


    def is3at(self, brd, n, x, y, dx, dy, player):
        """Return True if a line of identical tokens exists starting at (x,y) in direction (dx,dy)"""
        # Avoid out-of-bounds errors
        if ((x + (n-1) * dx >= brd.w) or
            (y + (n-1) * dy < 0) or (y + (n-1) * dy >= brd.h)):
            return False
        # Go through elements
        for i in range(1, n):
            if brd.board[y + i*dy][x + i*dx] != player:
                return False
        return True

        
#----------------------------------------------------------------------------- 

    def is_end(self, brd):
        """check if game over"""
        return brd.get_outcome() == 0

    def h(self, brd):
        """just check if any win then the other"""
        my, oppo = 0, 0
        for i in range(brd.w):
            for j in range(brd.h):
                if brd.is_any_line_at(i, j):  # if at a cell, exist a line to win
                    if brd.board[j][i] == self.player:
                        my += 1
                    else:
                        oppo += 1
        return my-oppo

    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ
