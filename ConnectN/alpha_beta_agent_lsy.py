import math
import agent

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
        inf = float('inf')
        best = -inf
        best_action = None

        for (nb, col) in self.get_successors(brd):      # check every successor
            v = self.max_value(nb, -inf, inf, self.max_depth)  # choose the worst case for the other player
            if v > best:
                best = v    # update best value
                best_action = col   # update action
        return best_action

    def min(self, brd, alpha, beta, depth):
        if self.is_end(brd):    # check if game over
            return self.h(brd)  # return score
        if depth == 0:          # check if no need more depth
            return self.h(brd)  # return score
        v = float('inf')
        for (nb, col) in self.get_successors(brd):
            v = min(v, self.max(nb, alpha, beta, depth-1))  # the other will choose the worst case for us
            if v <= alpha:
                return v    # return the value
            beta = min(beta, v) # update beta
        return v

    def max(self, brd, alpha, beta, depth):
        if self.is_end(brd):    # check if game over
            return self.h(brd)  # return score
        if depth == 0:          # check if no need more depth
            return self.h(brd)  # return score
        v = -float('inf')
        for (nb, col) in self.get_successors(brd):
            v = max(v, self.min(nb, alpha, beta, depth-1))  # the best case for us
            if v >= beta:
                return v
            alpha = max(alpha, v) # update alpha
        return v

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
