import sys
sys.path.insert(0, '../bomberman')
import math
from entity import CharacterEntity
from colorama import Fore, Back
from queue import PriorityQueue

maxDepth = 2
inf = float('inf')
ninf = -float('inf')
alertRange = 400
win = 90000000
lose = -90000000000

class TestCharacter(CharacterEntity):

    def do(self, wrld):
              
        c_position = (self.x, self.y)
        a_star_move = self.a_star_search(c_position, wrld)

      
        if a_star_move is not None:
            self.bestMove = a_star_move
      
        self.place_bomb() #place the bomb as soon as it is allowed
    
        (dx,dy) = self.advance_search(wrld, 0, None)
        self.move(dx,dy)
        
        pass


    def advance_search(self, wrld, depth, events):
        v = ninf
        act = (0,0)
        
        #terminal cases
        if depth != 0:
            for event in events: 
                if event.tpe == event.BOMB_HIT_CHARACTER or event.tpe == event.CHARACTER_KILLED_BY_MONSTER:
                # bomberman is dead
                    return lose
                elif event.tpe == event.CHARACTER_FOUND_EXIT:
                # bomberman is winning
                    return win
                
        if depth >= maxDepth:
            return self.final_utility(wrld)
       
        
        bman = next(iter(wrld.characters.values()))[0]
        
        ms = wrld.monsters.values()
        hasMonst = False
        
        # a logic to determine the closet threat of the monster
        if len(ms) == 1:
            hasMonst = True
            monst = next(iter(ms))[0]
        elif len(ms) == 2:                          
            hasMonst = True
            monst1 = next(iter(ms))[0]
            monst2 = next(iter(ms))[0]
            if max(monst1.x - bman.x, monst1.y - bman.y) > max(monst2.x - bman.x, monst2.y - bman.y):
                monst = monst2
            else:
                monst = monst1  
        
        moves = self.get_sucells(bman.x, bman.y, wrld)
        moves.append((0,0)) # make sure the bomberman has upmost 9 possible moves
        for cell in moves:
            bman.move(cell[0], cell[1])
            
            if hasMonst:
                move = 0
                move_val = 0
                
                for mcell in self.get_sucells(monst.x, monst.y, wrld):
                    monst.move(mcell[0], mcell[1])
                    move += 1
                    (newWrld, newEvents) = wrld.next()
                    move_val += self.advance_search(newWrld, depth+1, newEvents)
                
                if(depth == 0): #record the action instead of the value
                    dist_to_best = self.better_move((bman.x + cell[0], bman.y + cell[1]), self.bestMove)
                    temp = move_val / move - dist_to_best  
                    if temp > v:
                        act = (cell[0], cell[1])
                        v = temp
                else:
                     v = max(v, (move_val/move))
            
            else:
                (newWrld, newEvents) = wrld.next()
                if(depth == 0): #record the action instead of the value
                    dist_to_best = self.better_move((bman.x + cell[0], bman.y + cell[1]), self.bestMove)
                    temp = self.advance_search(newWrld, depth+1, newEvents) 
                    temp -= dist_to_best
                    if temp > v:
                        act = (cell[0], cell[1])
                        v = temp
                else:
                     v = max(v, self.advance_search(newWrld, depth+1, newEvents))
        
        if (depth == 0): #return the action instead of the value
            return act
        return v
            
        
       
    def get_sucells(self, x, y, wrld):
        cells = []
        if self.is_legal_move(x + 1, y, wrld):
            cells.append((1, 0))
        if self.is_legal_move(x - 1, y, wrld):
            cells.append((-1, 0))
        if self.is_legal_move(x, y + 1, wrld):
            cells.append((0, 1))
        if self.is_legal_move(x, y - 1, wrld):
            cells.append((0,-1))
        if self.is_legal_move(x + 1, y + 1, wrld):
            cells.append((1, 1))
        if self.is_legal_move(x + 1, y - 1, wrld):
            cells.append((1,-1))
        if self.is_legal_move(x - 1, y + 1, wrld):
            cells.append((-1, 1))
        if self.is_legal_move(x - 1, y - 1, wrld):
            cells.append((-1, -1))
 
        return cells
        
        
    def is_legal_move(self, x, y, wrld):
        if(x >= 0 and y >= 0 and x < wrld.width() and y < wrld.height()):
            if not wrld.wall_at(x, y):
                return True
        return False
    
    def better_move(self, moveA, moveB):
        (x1, y1) = moveA
        (x2, y2) = moveB
        betterMove = abs(x1 - x2) + abs(y1 - y2)
        return betterMove
    
    def final_utility(self, wrld):
        bman = next(iter(wrld.characters.values()))[0]
        utility = 0
        if len(wrld.monsters.values()) == 0: 
            return utility
        mls = next(iter(wrld.monsters.values()))
        for monst in mls:
            i = abs(bman.x - monst.x)
            j = abs(bman.y - monst.y)
            if i <= 2 and j <= 2:
                if i <= 1 and j <= 1:
                    utility -= 100000
                utility -= 10000
            utility -= alertRange / (i+j)**2
        return utility
#---------------------------------------------------------------------------------------

    def a_star_search(self, start, wrld):
        exitCell = wrld.exitcell
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        
        while not frontier.empty():
            currentNode = frontier.get()
            
            if currentNode == exitCell:
                previous = currentNode
                while came_from[previous] != start:
                    previous = came_from[previous]
                return previous
            
            # convert movement to node
            cells = self.get_sucells(currentNode[0], currentNode[1], wrld)
            neighbors = []
            for i in cells:
                neighbors.append((i[0]+currentNode[0], i[1]+currentNode[1]))
                
            for next in neighbors:
                new_cost = cost_so_far[currentNode] + 1  
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.astarH(exitCell, next)
                    frontier.put(next, priority)
                    came_from[next] = currentNode
                    
        
        
        return (start[0], start[1]+1)
        
            
    
    # Heuristic value for astar from on node to another
    # Since diagonal weight the same as straight line
    # the max of difference of a and y will be the Heuristic
    # Input: start node, end node
    # Output: Heuristic value in int
    def astarH(self, start, end):
        x = abs(start[0] - end[0])
        y = abs(start[1] - end[1])
        return max(x, y)


