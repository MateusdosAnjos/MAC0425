#Nome: Mateus Agostinho dos Anjos
#NUSP: 9298191

# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
      "You can initialize Q-values here..."
      ReinforcementAgent.__init__(self, **args)
      #Inicializacao dos qValores
      self.qValores = util.Counter()

    def getQValue(self, state, action):
      """
        Returns Q(state,action)
        Should return 0.0 if we have never seen a state
        or the Q node value otherwise
      """
      #se nao vimos o estado o valor sera 0.0
      return self.qValores[(state, action)]

    def computeValueFromQValues(self, state):
      """
        Returns max_action Q(state,action)
        where the max is over legal actions.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return a value of 0.0.
      """
      qVals = []
      #para cada acao legal, devemos computar o Qvalor
      for acao in self.getLegalActions(state):
        qVals.append(self.getQValue(state, acao))
      #Caso nao tenhamos acoes legais, caso do estado terminal,
      #devemos devolver 0.0  
      if len(self.getLegalActions(state)) == 0:
        return 0.0
      #caso contrario devolvemos o maximo  
      else:
        return max(qVals)

    def computeActionFromQValues(self, state):
      """
        Compute the best action to take in a state.  Note that if there
        are no legal actions, which is the case at the terminal state,
        you should return None.
      """
      #por enquanto nao temos melhor acao nem maxQVal
      melhorAcao = None
      maxQVal = 0
      #procurando para toda acao em acoes legais
      for acao in self.getLegalActions(state):
        #pegamos qVal pra tao acao
        qVal = self.getQValue(state, acao)
        #se for maior que o maximo ou se nao tivermos melhor acao ainda
        #este valor sera o maximo e sua acao sera a melhor
        if qVal > maxQVal or melhorAcao is None:
          maxQVal = qVal
          melhorAcao = acao
      return melhorAcao

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # escolhemos a acao
        acoesPoss = self.getLegalActions(state)
        acao = None
        if len(acoesPoss) == 0:
          return acao
        #para o epsilon em flipcoin  
        if util.flipCoin(self.epsilon):
          #pegamos acao randomica dentre as possiveis
          acao = random.choice(acoesPoss)
        #se nao, escolhemos a acao a partir dos Qvalores  
        else:
          acao = self.computeActionFromQValues(state)
        return acao

    def update(self, state, action, nextState, reward):
      """
        The parent class calls this to observe a
        state = action => nextState and reward transition.
        You should do your Q-Value update here

        NOTE: You should never call this function,
        it will be called on your behalf
      """
      primeiraEq = (1 - self.alpha) * self.getQValue(state, action)
      #se nao houverem acoes legais no proximo estado x sera a propria
      #recompensa
      if len(self.getLegalActions(nextState)) == 0:
        x = reward
      #caso contrario computamos o novo valor de x seguindo as equacoes
      #dadas  
      else:
        x = reward + (self.discount * max([self.getQValue(nextState, next_action) for next_action in self.getLegalActions(nextState)]))
      segundaEq = self.alpha * x
      self.qValores[(state, action)] = primeiraEq + segundaEq

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self, state)
        self.doAction(state, action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        vetorFeat = self.featExtractor.getFeatures(state, action)
        qValue = self.weights * vetorFeat
        return qValue

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        #implementa o que foi passado no enunciado
        diff = reward + self.discount * self.getValue(nextState) - self.getQValue(state, action)
        feats = self.featExtractor.getFeatures(state, action)
        for feature in feats:
          self.weights[feature] += self.alpha * diff * feats[feature]
          
    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
