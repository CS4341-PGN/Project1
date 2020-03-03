# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from queue import PriorityQueue

class TestCharacter(CharacterEntity):

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
    def astarH(start, end):
        x = abs(start[0] - end[0])
        y = abs(start[1] - end[1])
        return max(x, y)
            
        
        
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

