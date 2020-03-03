# This is necessary to find the main code
import sys
import math
import heapq

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

maxDepth = 2
inf = float('inf')
ninf = -float('inf')
sensitivity = 800
class TestCharacter(CharacterEntity):

    def do(self, wrld):
              
        c_position = (self.x, self.y)
        a_star_move = self.a_star_search(c_position, wrld.exitcell, wrld)

      
        if a_star_move is not None:
            self.bestmove = a_star_move[0]
      
        self.place_bomb()
    
        (dx,dy) = self.expectimax_search(wrld, 0, None)
        self.move(dx,dy)
        
        pass


    def expectimax_search(self, wrld, depth, events):
        v = ninf
        act = (0,0)
        #terminal cases
        
        if depth != 0:
            for event in events: 
                if event.tpe == event.BOMB_HIT_CHARACTER or event.tpe == event.CHARACTER_KILLED_BY_MONSTER:
                # character is dead so worst evaluation
                    return -90000000000
                elif event.tpe == event.CHARACTER_FOUND_EXIT:
                # character is winning so best evaluation
                    return 90000000
                
        if depth >= maxDepth:
            return self.final_utility(wrld)
       
        
        bman = next(iter(wrld.characters.values()))[0]#!!!!! 
        
        ms = wrld.monsters.values()
        hasMonst = False
        
        if len(ms) == 1:
            hasMonst = True
            monst = next(iter(ms))[0]
        elif len(ms) == 2:                          # when there are 2 monsters
            hasMonst = True
            monst1 = next(iter(ms))[0]
            monst2 = next(iter(ms))[0]
            if max(monst1.x - bman.x, monst1.y - bman.y) > max(monst2.x - bman.x, monst2.y - bman.y):
                monst = monst2
            else:
                monst = monst1  
        
        moves = self.get_sucells(bman.x, bman.y, wrld)
        moves.append((0,0))
        for cell in moves:
            bman.move(cell[0], cell[1])
            
            if hasMonst:
                move = 0
                move_val = 0
                
                for mcell in self.get_sucells(monst.x, monst.y, wrld):
                    monst.move(mcell[0], mcell[1])
                    move += 1
                    (newWrld, newEvents) = wrld.next()
                    move_val += self.expectimax_search(newWrld, depth+1, newEvents)
                
                if(depth == 0):
                    dist_to_best = self.heuristic((bman.x + cell[0], bman.y + cell[1]), self.bestmove)
                    temp = move_val / move - dist_to_best  
                    if temp > v:
                        act = (cell[0], cell[1])
                        v = temp
                else:
                     v = max(v, (move_val/move))
            
            else:
                (newWrld, newEvents) = wrld.next()
                if(depth == 0):
                    dist_to_best = self.heuristic((bman.x + cell[0], bman.y + cell[1]), self.bestmove)
                    temp = self.expectimax_search(newWrld, depth+1, newEvents) 
                    temp -= dist_to_best
                    if temp > v:
                        act = (cell[0], cell[1])
                        v = temp
                else:
                     v = max(v, self.expectimax_search(newWrld, depth+1, newEvents))
        
        if (depth == 0):
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

#---------------------------------------------------------------------------------------
    def empty_cell_neighbors(self, node, wrld):
        # List of empty cells
        cells = []
        # Go through neighboring cells
        for dx in [-1, 0, 1]:
            # Avoid out-of-bounds access
            if (node[0] + dx >= 0) and (node[0] + dx < wrld.width()):
                for dy in [-1, 0, 1]:
                    # Avoid out-of-bounds access
                    if (node[1] + dy >= 0) and (node[1] + dy < wrld.height()):
                        # Is this cell safe?
                        if wrld.exit_at(node[0] + dx, node[1] + dy) or wrld.empty_at(node[0] + dx, node[1] + dy):
                            # Yes
                            if not (dx is 0 and dy is 0):
                                cells.append((node[0] + dx, node[1] + dy))
        # All done
        return cells


    # heuristic from one location to another
    # node is just a tuple with (x, y)
    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    # param: start is a start node as tuple (x, y)
    #        goal is a goal node as tuple (x, y)
    #        wrld is the current world
    # return: the best next node towards exit
    def a_star_search(self, start, goal, wrld):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in self.empty_cell_neighbors(current, wrld):
                new_cost = cost_so_far[current] + 1  # cost from one node to its neighbor is 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

        min = math.inf
        # search if we can reach goal
        for next in came_from:
            dis_to_goal = self.heuristic(next, goal)
            if dis_to_goal < min:
                min = dis_to_goal
                min_to_exit = next
        if next == goal:
            # we can reach goal
            while came_from[next] is not None:
                self.set_cell_color(next[0], next[1], Fore.RED + Back.RED)
                if came_from[next] == start:
                    return next, "has path to exit"  # next move from start to in the A* path
                next = came_from[next]

        while came_from[min_to_exit] is not None:
            self.set_cell_color(min_to_exit[0], min_to_exit[1], Fore.RED + Back.RED)
            if came_from[min_to_exit] == start:
                return min_to_exit, "no path to exit"  # next move from start to in the A* path
            min_to_exit = came_from[min_to_exit]

        # goal can not be reached
        # return a move that get close to the goal
        return None
    
    def final_utility(self, wrld):
        c = next(iter(wrld.characters.values()))
        c = c[0]
        return self.eval1(wrld, c)

    # Evaluate world based on:
    #   1. distance to monster
    #   2. 
    def eval1(self, wrld, c):
        if len(wrld.monsters.values()) == 0: return 0
        mlist = next(iter(wrld.monsters.values()))
        score = 0
        for m in mlist:
            distx = abs(c.x - m.x)
            disty = abs(c.y - m.y)
            if distx <= 2 and disty <= 2:
                if distx <= 1 and disty <= 1:
                    score -= 100000
                score -= 10000
            score -= sensitivity / (distx+disty)**2
        return score

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]
