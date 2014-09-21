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
    # return ['A']
    # [state, action, g_cost, f_cost]

    # start_state = [problem.getStartState(), [], 0, f_, 
    # start_state = problem.getStartState()
    g_cost = 0
    f_cost = g_cost + heuristic(problem.getStartState(), problem)
    start_state = [problem.getStartState(), [], g_cost, f_cost] 
    open_set = [start_state]
    closed_set = []

    while open_set:
        current = returnLowestFcost(open_set)
        print "current"
        print current

        if problem.isGoalState(current[0]):
            return current[1]
        open_set = removeListFrom2DList(open_set, current)
        closed_set.append(current)
        for (successor, action, cost) in problem.getSuccessors(current[0]):
            if existsInLists(successor, closed_set):
                continue

            tentative_g_cost = current[2] + cost
            # print tentative_g_cost
            #  need to optimized!!
            sucessor_already_visited = existsInLists(successor, open_set)
            if sucessor_already_visited:
                if tentative_g_cost < sucessor_already_visited[2]:
                    removeListFrom2DList(open_set, sucessor_already_visited)

            if not existsInLists(successor, open_set) or tentative_g_cost < sucessor_already_visited[2]:
                successor_f_cost = tentative_g_cost + heuristic(successor, problem)
                actions = current[1] + [action]
                successor_state = [successor, actions, tentative_g_cost, successor_f_cost]
                print "successor_state"
                print successor_state
                if not existsInLists(successor, open_set):
                    open_set.append(successor_state)

    print "A* search failed"
    return "failure"

def removeListFrom2DList(doubleList, target):
    for i in range(0, len(doubleList)):
        if doubleList[i] == target:
            del doubleList[i]
            return doubleList
    print "something is wrong!!"
    return False

def existsInLists(state, doubleList):
    for li in doubleList:
        if state == li[0]:
            return li
    return False

# def returnExistsInLists(state, doubleList):
#     for li in doubleList:
#         if state == li[0]:
#             return li
#     return False

def returnLowestFcost(open_set):
    answer = []
    minimum = float("inf")
    for li in open_set:
        if li[3] < minimum:
            minimum = li[3]
            answer = li
    if answer:
        return answer
    else:
        print "something is wrong. List shouldn't be empty"



# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
