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
        P = brd.player
        #print("ab player:", brd.player)
        ctr = 0
        return self.Alpha_Beta(brd, P, ctr)

    # def heuristic1(self, brd, P):
    #     """Do the alpha beta pruning and prediction"""
    #     succ = self.get_successors(brd)
    #     max_score = 0
    #     the_col = int (brd.n / 2)
    #     for tup in succ:
    #         temp = self.total_score(brd, P)
    #
    #         if(max_score < temp):
    #             the_col = tup[1]
    #
    #     return the_col

    def Alpha_Beta(self, brd, P, ctr):
        alpha = -10000
        beta = 10000
        res = self.AB_max(brd, P, alpha, beta, ctr)
        v = res[0]
        col = res[1]
        return col


    # Alpha-Beta Pruning

    # Minimax : Max Algorithm for player itself
    # ctr is the counter of the depth
    def AB_max(self, brd, P, alpha, beta, ctr):

        if ctr == 0:
            the_col = self.check_oppo(brd, P)
            if the_col != -1:
                #print("THeCOL: ", the_col)
                return 10000, the_col

        #print("MAXAB is: ", alpha, " ", beta)

        if self.terminal_test(brd, ctr):
            res = (self.heuristic(brd, P), -1)
            return res
        v = -10000
        succ = self.get_successors(brd)

        # store max value into v
        col = -1
        for tup in succ:
            #print("MAX col in new turn: ", col)

            # counter add one
            min_res = self.AB_min(tup[0], P, alpha, beta, ctr + 1)
            min_ed = min_res[0]

            # Max-ed
            if min_ed >= v:
                v = min_ed

            if v > beta:
                #print("v beta", v, beta)
                res = (v, -1)
                return res

            #print("MAX, V, ALpha: ", v, alpha)
            if v > alpha:
                alpha = v
                col = tup[1]

        # the return value result has two tuples
        # the first one represents the value of v
        # the second one represents the action that will lead to the direction of the v
        res = (v, col)
        #print("v col is-----------------------------------------------------------------", v, col)

        return res

    # Minimax: Min Algorithm for opponent
    # ctr is the counter of the depth
    def AB_min(self, brd, P, alpha, beta, ctr):
        #print("MINAB is: ", alpha, " ", beta)
        if self.terminal_test(brd, ctr):
            sc = self.heuristic(brd, P)
            #print("The min score is: ", sc)
            res = (sc, -1)
            return res
        v = 10000
        succ = self.get_successors(brd)

        # store min value into v
        col = -1
        for tup in succ:
            #print("MIN col in new turn: ", col)
            # counter add one
            max_res = self.AB_max(tup[0], P, alpha, beta, ctr + 1)
            max_ed = max_res[0]
            #print("Max_ed: ", max_ed)

            # Min-ed
            if max_ed <= v:
                v = max_ed

            if v < alpha:
                #print("V alpha", v, alpha)
                res = (v, -1)
                return res

            if v < beta:
                beta = v
                col = tup[1]

        res = (v, col)

        return res

    # find out the score of the target player of the situation
    # Put all token (AB and opponents' together
    # P is the player of AB (Alpha-Beta Agent)

    def check_oppo(self, brd, P):
        for x in range(brd.w):
            for y in range(brd.h):
                the_col = self.check_oppo_line(brd, x, y, P, 0, 1)
                if the_col != -1:
                    return the_col
                the_col = self.check_oppo_line(brd, x, y, P, 1, 0)
                if the_col != -1:
                    return the_col
                the_col = self.check_oppo_line(brd, x, y, P, 1, 1)
                if the_col != -1:
                    return the_col
                the_col = self.check_oppo_line(brd, x, y, P, 1, -1)
                if the_col != -1:
                    return the_col
        return -1

    def check_oppo_line(self, brd, x, y, P, dx, dy):

        if P == 1:
            o = 2
        else:
            o = 1

        cnt_less = 0
        for i in range(brd.n - 1):
            if y + i*dy <= brd.h - 1 and x + i*dx <= brd.w - 1:
                if brd.board[y + i*dy][x + i*dx] == o:

                    cnt_less = cnt_less + 1
            else:
                break

        if cnt_less == brd.n - 1:
            for i in range(brd.n):
                if y + i * dy <= brd.h - 1 and x + i * dx <= brd.w - 1:     #check availability

                    if brd.board[y + i * dy][x + i * dx] == 0:      #check blank position

                        if y + i*dy - 1 >= 0:                       #check availability

                            if brd.board[y + i*dy - 1][x + i*dx] != 0:  #check grid below the point
                                return x + i*dx

        if cnt_less == brd.n - 2:
            for i in range(brd.n - 1):

                if y + i * dy <= brd.h - 1 and x + i * dx <= brd.w - 1:     #check availability
                    if brd.board[y + i * dy][x + i * dx] == 0:      #check blank position
                        if y + i*dy - 1 >= 0:                       #check availability
                            if brd.board[y + i*dy - 1][x + i*dx] != 0:  #check grid below the point
                                return x + i*dx

        return -1

    # def check_oppo_line(self, brd, x, y, P, dx, dy):
    #     cnt_less_2 = True
    #     cnt_less_1 = True
    #
    #
    #     # check if there is connection that has 2 tokens less than the requirement
    #     for i in range(brd.n - 2):
    #         if ((x + (brd.n - 1) * dx >= brd.w) or
    #                 (y + (brd.n - 1) * dy < 0) or (y + (brd.n - 1) * dy >= brd.h)):
    #             break
    #
    #         if brd.board[y + i*dy][x + i*dx] != P:
    #             cnt_less_2 = False
    #
    #     for i in range(brd.n - 1):
    #         if ((x + (brd.n - 1) * dx >= brd.w) or
    #                 (y + (brd.n - 1) * dy < 0) or (y + (brd.n - 1) * dy >= brd.h)):
    #             break
    #
    #         if brd.board[y + i *dy][x + i*dx] != P:
    #             cnt_less_1 = False
    #
    #     # if there are, then check whether they are threatening
    #
    #     if cnt_less_2:
    #         if y - dy > 0 and x - dx > 0:                                 # check the blank availability
    #                 if brd.board[y - dy][x - dx] == 0 and brd.board[y - dy - 1][x - dx] != 0:   #
    #                     return x - dx
    #
    #         elif y + (brd.n - 2)*dy < brd.h and x + (brd.n - 2)*dx < brd.w:
    #                 if brd.board[y + (brd.n - 2)*dy][x + (brd.n - 2)*dx] == 0 and brd.board[y + (brd.n - 2)*dy - 1][x + (brd.n - 2)*dx] != 0:
    #                     return x + (brd.n - 2) * dx
    #
    #     if cnt_less_1:
    #         if y - dy > 0 and x - dx > 0:                                 # check the blank availability
    #                 if brd.board[y - dy][x - dx] == 0 and brd.board[y - dy - 1][x - dx] != 0:   #
    #                     return x - dx
    #
    #         elif y + (brd.n - 1)*dy < brd.h and x + (brd.n - 1)*dx < brd.w:
    #                 if brd.board[y + (brd.n - 1)*dy][x + (brd.n - 1)*dx] == 0 and brd.board[y + (brd.n - 1)*dy - 1][x + (brd.n - 1)*dx] != 0:
    #                     return x + (brd.n - 1) * dx
    #
    #     return -1

    def heuristic(self, brd, P):
        #brd.print_it()
        # Total score = self score - opponent score
        own = 0
        oppo = 0
        for x in range(brd.w):
            # print("brd.w - brd.n + 1:", brd.w - brd.n + 1)
            for y in range(brd.h):

                # print("brd.h - brd.n + 1:", brd.h - brd.n + 1)
                own = own + self.score_in_token(brd, x, y, P)

        if(P == 1):
            O = 2
        else:
            O = 1

        #print("The opponent player is: ", O)
        for y in range(brd.w):
            # print("brd.w - brd.n + 1:", brd.w - brd.n + 1)
            for y in range(brd.h):
                # print("brd.h - brd.n + 1:", brd.h - brd.n + 1)
                oppo = oppo + self.score_in_token(brd, x, y, O)

        #print("Own: " , own, " Oppo: ", oppo)

        return own - oppo * 2

    # Since the heuristic function will be only executed on the free columns
    # that we do not have to worry about the problem
    # that the new token is put out of the board
    # def score_in_line(self, brd, x, y, P, dx, dy):
    #     p1 = 0
    #     # Get the current player (self)
    #     t = P
    #
    #     # Go through elements
    #     for i in range(1, brd.n):
    #         # Check if out of bound
    #         if ((x + (brd.n - 1) * dx >= brd.w) or
    #                 (y + (brd.n - 1) * dy < 0) or (y + (brd.n - 1) * dy >= brd.h)):
    #             break
    #         elif brd.board[y + i*dy][x + i*dx] == t:
    #             p1 = p1 + 1
    #
    #     return p1

    def score_in_line(self, brd, x, y, P, dx, dy):
        max_cons = 0
        cons = 0
        score = 0
        t = P
        if P == 1:
            o = 2
        else:
            o = 1

        max = brd.w
        if brd.h > brd.w:
            max = brd.h

        for i in range(max):
            if y + i * dy <= brd.h - 1 or x + i * dx <= brd.w - 1:
                break
            else:
                if brd.board[y + i * dy][x + i * dx] == t:
                    cons =+ 1
                    if cons > max_cons:
                        max_cons = cons
                elif brd.board[y + i*dy][x + i*dx] == 0:
                    score =+ (2 ^ cons)
                    cons = 0
                elif brd.board[y + i*dy][x + i*dx] != o:
                    score =+ int (2 ^ cons) / 2
                    cons = 0

        return score




    # Check the score of the player in current state
    def score_in_token(self, brd, x, y, P):
        return (self.score_in_line(brd, x, y, P, 1, 0) *
                self.score_in_line(brd, x, y, P, 0, 1) *
                self.score_in_line(brd, x, y, P, 1, 1) *
                self.score_in_line(brd, x, y, P, 1, -1))

    # Check whether the action will lead to a end in the game / or the Minimax algorithm
    # if max_depth is reached, jumped out
    def terminal_test(self, brd, ctr):
        if ctr >= self.max_depth:
            return True
        freecols = brd.free_cols()
        if not freecols:
            return True

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


THE_AGENT = AlphaBetaAgent("WangYizhen", 4)
