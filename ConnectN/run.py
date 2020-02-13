import random
import game
import agent
import alpha_beta_agent as aba
import alpha_beta_agentYZ as abaYZ


# Set random seed for reproducibility
random.seed(1)

#
# Random vs. Random
#
#g = game.Game(7, # width
#              6, # height
#              4, # tokens in a row to win
#              agent.RandomAgent("random1"),       # player 1
#              agent.RandomAgent("random2"))       # player 2

#
# Human vs. Random
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human"),    # player 1
#               agent.RandomAgent("random"))        # player 2

#
# Random vs. AlphaBeta
##
#g = game.Game(7, # width
#              6, # height
#              4, # tokens in a row to win
#              agent.RandomAgent("random"),        # player 1
#              aba.AlphaBetaAgent("alphabeta", 5)) # player 2

# Alphabeta vs. AlphaBeta
#
g = game.Game(7, # width
              6, # height
              4, # tokens in a row to win
              aba.AlphaBetaAgent("alphabeta", 5),        # player 1
              aba.AlphaBetaAgent("alphabeta2", 5)) # player 2

#
## Human vs. AlphaBeta
##
#g = game.Game(7, # width
#              6, # height
#              4, # tokens in a row to win
#              agent.InteractiveAgent("human"),    # player 1
#              aba.AlphaBetaAgent("alphabeta", 5)) # player 2

## Alphabeta vs. Human
##
#g = game.Game(7, # width
#              6, # height
#              4, # tokens in a row to win
#              aba.AlphaBetaAgent("alphabeta", 5),
#              agent.InteractiveAgent("human")) # player 2

#
# Human vs. Human
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human1"),   # player 1
#               agent.InteractiveAgent("human2"))   # player 2

## Alphabeta vs. Yizhen
#
#g = game.Game(7, # width
#              6, # height
#              4, # tokens in a row to win
#              aba.AlphaBetaAgent("alphabeta", 5),
#              abaYZ.AlphaBetaAgent("WYZ", 5)) # player 2

# Execute the game
outcome = g.go()
