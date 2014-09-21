"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import sys
import copy

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

    #(successor, action, stepCost)
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

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.

    You are not required to implement this, but you may find it useful for Q5.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0



def iterativeDeepeningSearch(problem):
    """
    Perform DFS with increasingly larger depth.

    Begin with a depth of 1 and increment depth by 1 at every step.
    """
    depth = 0
    # for d in range(0, ):
    while True:
        result = depthLimitedSearch(problem, depth)
        # print result
        if result != "cutoff":
            return result
        depth += 1

def depthLimitedSearch(problem, limit):
    """
    Helper function and DLS algorithm for iterativeDeepeningSearch
    """
    # print "STARTING RDLS"
    # print "RDLS: " + problem.getStartState()
    # return recursiveDls(problem.getStartState(), [], problem, limit, [problem.getStartState()], set(problem.getStartState()))
    return recursiveDls(problem.getStartState(), [], problem, limit, set(problem.getStartState()))

# returns a list of actions to goal node
def recursiveDls(node, actions, problem, limit, visited):
    cutoff = "cutoff"
    failure = "failure"
    if problem.isGoalState(node):
        return actions
    elif limit == 0:
        return cutoff
    else:
        cutoff_occured = False
        children = []
        for child in problem.getSuccessors(node):
            if child[0] not in visited:
                children.append(child)
                visited.add(child[0])
        for (successor, action, cost) in children:
            result = recursiveDls(successor, [action], problem, limit - 1, visited)
            if result == cutoff:
                cutoff_occured = True
            elif result != failure:
                return actions + result
        if cutoff_occured:
            return cutoff
        else:
            return failure


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    start_state = problem.getStartState();
    open_set = set(start_state)
    closed_set = set()
    g_cost = 0
    h_cost = g_cost + heuristic(start_state, problem)

    while open_set:
        current = 

def returnLowestFcost



# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
