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
