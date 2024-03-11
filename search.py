# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    visited = dict()
    start_node = (problem.getStartState(),[])
    return dfs_aux(problem,start_node,visited)  
    util.raiseNotDefined()

def dfs_aux(problem:SearchProblem,node,visited) -> list: 
    if problem.isGoalState(node[0]): return node[1]
    visited[node[0]] = True
    for neighbor in problem.getSuccessors(node[0]):
        child = neighbor[0]
        action = neighbor[1]
        if not visited.get(child):
            new_path = node[1] + [action]
            child_node = (child,new_path) # (State,action)
            result = dfs_aux(problem,child_node,visited)
            if result: # If list isn't empty, you found a path - return it. 
                return result
    return []
        


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    Q = util.Queue()
    visited = dict()
    start_node = (problem.getStartState(),[])
    Q.push(start_node)
    while not Q.isEmpty():
        node = Q.pop()
        if problem.isGoalState(node[0]): return node[1]
        if not visited.get(node[0]): # If not visited, add to visited and expand
            visited[node[0]] = True
            for neighbor in problem.getSuccessors(node[0]):
                child = neighbor[0]
                action = node[1] + [neighbor[1]]
                child_node = (child,action)
                Q.push(child_node)
    return []
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    Q = util.PriorityQueue()
    visited = dict()
    path_cost = dict()
    start = problem.getStartState()
    start_node = (start,[],0)
    Q.push(start_node,0)
    visited[start] = True
    path_cost[start] = 0
    while not Q.isEmpty():
        node = Q.pop()
        if problem.isGoalState(node[0]): return node[1]
        else: 
            for neighbor in problem.getSuccessors(node[0]):
                child = neighbor[0]
                new_path = node[1] + [neighbor[1]] 
                new_cost = problem.getCostOfActions(new_path)
                if not visited.get(child) or less_cost(child,path_cost,new_cost): # If new path less than previous, update
                    visited[child] = True
                    path_cost[child] = new_cost
                    child_node = (child,new_path,new_cost)
                    Q.push(child_node,new_cost)
    return []
    util.raiseNotDefined()

def less_cost(state, path_cost, new_cost):
        old_cost = path_cost.get(state, -1)
        if old_cost == -1:
            return True
        else:
            return new_cost < old_cost

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    Q = util.PriorityQueue()
    visited = dict()
    path_cost = dict()
    start = problem.getStartState()
    start_node = (start,[],0)
    Q.push(start_node,0)
    visited[start] = True
    path_cost[start] = 0
    while not Q.isEmpty():
        node = Q.pop()
        if problem.isGoalState(node[0]): return node[1]
        else: 
            for neighbor in problem.getSuccessors(node[0]):
                child = neighbor[0]
                new_path = node[1] + [neighbor[1]] 
                new_cost = problem.getCostOfActions(new_path) + heuristic(neighbor[0],problem)
                if not visited.get(child) or less_cost(child,path_cost,new_cost): # If new path less than previous, update
                    visited[child] = True
                    path_cost[child] = new_cost
                    child_node = (child,new_path,new_cost)
                    Q.push(child_node,new_cost)
    return []
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
