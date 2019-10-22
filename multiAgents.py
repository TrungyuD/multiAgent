# multiAgents.py
# --------------
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
        successorGameState = currentGameState.generatePacmanSuccessor(action) #next state of pacman
        newPos = successorGameState.getPacmanPosition() #new position of pacman
        newFood = successorGameState.getFood() #list food exist of map
        newGhostStates = successorGameState.getGhostStates() #get state of ghost 
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        value = successorGameState.getScore() 

        distanceToFirstGhost = manhattanDistance(newPos, newGhostStates[0].getPosition()) 
        if distanceToFirstGhost > 0:
            value -= 10.0 / distanceToFirstGhost

        distancesToFood = [manhattanDistance(newPos, x) for x in newFood.asList()]
        if len(distancesToFood):
            value += 10.0 / min(distancesToFood)

        return value

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
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

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
      Your minimax agent (question 2)
    """

    def determineAction(self, gameState, depth, agentIndex=0):

        # return score of finish gamestate 
        if gameState.isWin() or gameState.isLose() or depth == 0:
          return (self.evaluationFunction(gameState),)

        numberOfGhosts = gameState.getNumAgents()

        if agentIndex == numberOfGhosts - 1:  # if is finish ghost, reduce depth - 1
            currentDepth = depth - 1
        else:
            currentDepth = depth  # else return currentDepth
        myIndex = (agentIndex + 1) % numberOfGhosts

        possibleActions = [
            (self.determineAction(gameState.generateSuccessor(agentIndex, i), currentDepth, myIndex)[0], i) for i in
            gameState.getLegalActions(agentIndex)]
        # return list action
        print possibleActions
        if (agentIndex != 0):  # if ghost return min
            minOfList = min(possibleActions)
            return minOfList
        else:
            maxOfList = max(possibleActions)
            return maxOfList  # if pacman return max

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
        "*** YOUR CODE HERE ***"
        return self.determineAction(gameState, self.depth)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    "*** YOUR CODE HERE ***"
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        depth = 0
        alpha = float('-inf')
        beta = float('inf')
        return self.getMaxValue(gameState, alpha, beta, depth)[1]

    def getMaxValue(self, gameState, alpha, beta, depth, agent = 0):
        actions = gameState.getLegalActions(agent)

        if not actions or gameState.isWin() or depth >= self.depth:
            return self.evaluationFunction(gameState), Directions.STOP

        successorCost = float('-inf')
        successorAction = Directions.STOP

        for action in actions:
            successor = gameState.generateSuccessor(agent, action)

            cost = self.getMinValue(successor, alpha, beta, depth, agent + 1)[0]

            if cost > successorCost:
                successorCost = cost
                successorAction = action

            if successorCost > beta:
                return successorCost, successorAction

            alpha = max(alpha, successorCost)

        return successorCost, successorAction

    def getMinValue(self, gameState, alpha, beta, depth, agent):
        actions = gameState.getLegalActions(agent)

        if not actions or gameState.isLose() or depth >= self.depth:
            return self.evaluationFunction(gameState), Directions.STOP

        successorCost = float('inf')
        successorAction = Directions.STOP

        for action in actions:
            successor = gameState.generateSuccessor(agent, action)

            if agent == gameState.getNumAgents() - 1:
                cost = self.getMaxValue(successor, alpha, beta, depth + 1)[0]
            else:
                cost = self.getMinValue(successor, alpha, beta, depth, agent + 1)[0]

            if cost < successorCost:
                successorCost = cost
                successorAction = action

            if successorCost < alpha:
                return successorCost, successorAction

            beta = min(beta, successorCost)

        return successorCost, successorAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        def expectimaxSearch(state, agentIndex, depth):
            # Neu la ghost cuoi dung
            if agentIndex == state.getNumAgents():
              # neu la max depth
              if depth == self.depth:
                return self.evaluationFunction(state)
              # tao max layer voi depth = depth + 1
              else:
                return expectimaxSearch(state, 0, depth + 1)
            else:
              moves = state.getLegalActions(agentIndex)
              if len(moves) == 0:
                return self.evaluationFunction(state)
              next = [expectimaxSearch(state.generateSuccessor(agentIndex, move), agentIndex + 1, depth) for move in moves]

              if agentIndex == 0:
                return max(next)
              else:
                # khong dung min nua ma dung avg
                return sum(next) / len(next)

        result = max(gameState.getLegalActions(0),
                     key=lambda x: expectimaxSearch(gameState.generateSuccessor(0, x), 1, 1))

        return result
        # util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newCapsules = currentGameState.getCapsules()

    ghostDistance = 0
    capsuleScore = 0
    if len(currentGameState.getCapsules()) != 0:
        closestCapsule = min([manhattanDistance(capsule, newPos) for capsule in currentGameState.getCapsules()]) 
        capsuleScore += 200 / closestCapsule

    closestghost = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]) 
    foodList = newFood.asList()
    if len(foodList) != 0:
        closestfood = min([manhattanDistance(newPos, food) for food in foodList])
    else:
        closestfood = 0

    if (ghost.scaredTimer != 0):
        capsuleScore = -300
        if closestghost <= 1:
            ghostDistance += 350
        else:
            ghostDistance = 250 / closestghost
        score = (-1.3 * closestfood) + ghostDistance - (3 * len(foodList)) + capsuleScore
    else:
        if closestghost <= 1:
            ghostDistance -= 1000
        else:
            ghostDistance = - 13 / closestghost
        score = (-1.3 * closestfood) + ghostDistance - (95 * len(foodList)) + capsuleScore
    return score

# Abbreviation
better = betterEvaluationFunction

