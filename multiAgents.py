# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions

        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        currentPacPos = currentGameState.getPacmanPosition()
        newPacPos = successorGameState.getPacmanPosition()
        currentFood = currentGameState.getFood()

        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


        evaluation = 0
        # print "newPacPos"
        # print(newPacPos)
        for ghostState in newGhostStates:
          # print "ghostPos"
          # print(ghostState.getPosition())
          if isNextTo(newPacPos, ghostState.getPosition()):
            if ghostState.scaredTimer > 0:
              evaluation += 500
            else:
              evaluation -= 1000
          if isOn(newPacPos, ghostState.getPosition()):
            if ghostState.scaredTimer > 0:
              evaluation += 500
            else:
              evaluation -= 1000
        # print "food"
        # print(newFood.asList())
        for food in currentFood.asList():
          if isOn(newPacPos, food):
            evaluation += 50

        if (successorGameState.getScore() > currentGameState.getScore):
          evaluation += 50

        if evaluation >= 0:
          nearestFood = findNearestFood(currentPacPos, currentFood.asList())
          # print(nearestFood)
          if (manhattanDistanceBetweenPoints(nearestFood, currentPacPos) > 
            manhattanDistanceBetweenPoints(nearestFood, newPacPos)):
            evaluation += 500
          # head towards food

        return evaluation

def isNextTo(obj1, obj2):
  nearX = (abs(obj1[0]-obj2[0]) == 1) and (obj1[1] == obj2[1])
  nearY = (abs(obj1[1]-obj2[1]) == 1) and (obj1[0] == obj2[0])
  # diagonal = True
  diagonal = (abs(obj1[1] - obj2[1]) == 1) and (abs(obj1[0] - obj2[0]) == 1)
  if (nearX or nearY) and not diagonal:
    # print ("obj 1 is at position " + str(obj1))
    # print ("obj 2 is at position " + str(obj2))
    return True
  else:
    return False

def isOn(obj1, obj2):
  if (obj1[0] == obj2[0]) and (obj1[1] == obj2[1]):
    return True
  else:
    return False

def findNearestFood(position, foods):
    closestDistance = -1
    index = -1
    for i in range(len(foods)):
        distance = manhattanDistanceBetweenPoints(position, foods[i])
        if distance > 0 and (index == -1 or distance <= closestDistance):
            index = i
            closestDistance = distance
    if (index != -1):
        return foods[index]
    else:
        return ()

def manhattanDistanceBetweenPoints(point1, point2):
    return abs(point1[0]-point2[0]) + abs(point1[1]-point2[1])

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 7)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(0)

        best_move = legalMoves[0]
        best_score = float('-inf')
        for move in legalMoves:
            clone = gameState.generateSuccessor(0, move)
            score = self.min_play(clone, gameState.getNumAgents(), 0, 0)
            # print score
            if score > best_score:
                best_move = move
                best_score = score
        # print best_score
        return best_move

    def min_play(self, game_state, num_agents, prev_agent, count):
        newAgent = (prev_agent+1)%num_agents
        if (len(game_state.getLegalActions(newAgent)) == 0) or ((count+1)%(game_state.getNumAgents()*self.depth) == 0):
            return scoreEvaluationFunction(game_state)
        moves = game_state.getLegalActions(newAgent)
        best_score = float('inf')
        for move in moves:
            clone = game_state.generateSuccessor(newAgent, move)
            if (newAgent+1)%num_agents == 0:
              score = self.max_play(clone, num_agents, newAgent, count+1)
            else:
              score = self.min_play(clone, num_agents, newAgent, count+1)
            if score < best_score:
                best_move = move
                best_score = score
        return best_score

    def max_play(self, game_state, num_agents, prev_agent, count):
        newAgent = (prev_agent+1)%num_agents
        if (len(game_state.getLegalActions(newAgent)) == 0) or ((count+1)%(game_state.getNumAgents()*self.depth) == 0):
            return scoreEvaluationFunction(game_state)
        moves = game_state.getLegalActions(newAgent)
        best_score = float('-inf')
        for move in moves:
            clone = game_state.generateSuccessor(newAgent, move)
            if (newAgent+1)%num_agents == 0:
              score = self.max_play(clone, num_agents, newAgent, count+1)
            else:
              score = self.min_play(clone, num_agents, newAgent, count+1)
            if score > best_score:
                best_move = move
                best_score = score
        return best_score

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 8)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """

        legalMoves = gameState.getLegalActions(0)

        best_move = legalMoves[0]
        best_score = float('-inf')
        for move in legalMoves:
            clone = gameState.generateSuccessor(0, move)
            score = self.min_play(clone, gameState.getNumAgents(), 0, 0)
            # print score
            if score > best_score:
                best_move = move
                best_score = score
        # print best_score
        return best_move


    def min_play(self, game_state, num_agents, prev_agent, count):
        newAgent = (prev_agent+1)%num_agents
        moves = game_state.getLegalActions(newAgent)
        if (len(game_state.getLegalActions(newAgent)) == 0) or ((count+1)%(game_state.getNumAgents()*self.depth) == 0):
            finalEval = scoreEvaluationFunction(game_state)
            return finalEval  
        best_score = float('inf')
        total_mini_score = 0
        for move in moves:
            clone = game_state.generateSuccessor(newAgent, move)
            if (newAgent+1)%num_agents == 0:
              total_mini_score += self.max_play(clone, num_agents, newAgent, count+1)
            else:
              total_mini_score += self.min_play(clone, num_agents, newAgent, count+1)
        # print(total_mini_score)
        return float(total_mini_score) / float(len(moves))

    def max_play(self, game_state, num_agents, prev_agent, count):
        newAgent = (prev_agent+1)%num_agents
        moves = game_state.getLegalActions(newAgent)
        if (len(game_state.getLegalActions(newAgent)) == 0) or ((count+1)%(game_state.getNumAgents()*self.depth) == 0):
            finalEval = scoreEvaluationFunction(game_state)
            return finalEval
        best_score = float('-inf')
        for move in moves:
            clone = game_state.generateSuccessor(newAgent, move)
            if (newAgent+1)%num_agents == 0:
              score = self.max_play(clone, num_agents, newAgent, count+1)
            else:
              score = self.min_play(clone, num_agents, newAgent, count+1)
            if score > best_score:
                best_move = move
                best_score = score
        return best_score

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 9).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

