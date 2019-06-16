#Nome: Mateus Agostinho dos Anjos
#NUSP: 9298191

# valueIterationAgents.py
# -----------------------
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


import mdp, util
from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        #efetuaremos o numero de iteracoes passada
        for i in range(self.iterations):
          #faremos uma copia do valor atual
          valorAtual = self.values.copy()
          #para cada estado
          for estado in self.mdp.getStates():
            #pegamos a lista de acoesPoss(iveis), lista para
            #os valores e as transicoes
            acoesPoss = self.mdp.getPossibleActions(estado)
            listaValores = []
            transicoes = []
            #caso base se for um terminal
            if self.mdp.isTerminal(estado):
              self.values[estado] = 0
            #Vamos calcular o mdp    
            else:
              #para cada acao possivel
              for acao in acoesPoss:
                #pegamos as transicoes do estado
                transicoes = self.mdp.getTransitionStatesAndProbs(estado, acao)
                valor = 0
                #para cada transicao
                for trans in transicoes:
                  #computamos o valor, seguindo o processo MDP
                  valor += trans[1]*(self.mdp.getReward(estado, acao, trans[0]) + self.discount * valorAtual[trans[0]])
                listaValores.append(valor)
              #pegamos o maior valor calculado    
              self.values[estado] = max(listaValores)
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        #Implementacao da formula do Qvalor
        valor = 0
        transicoes = self.mdp.getTransitionStatesAndProbs(state, action)
        for trans in transicoes:
             valor += trans[1]*(self.mdp.getReward(state, action, trans[0]) + self.discount * self.values[trans[0]])
        return valor

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        #quando eh estado terminal nao temos acao a executar
        if self.mdp.isTerminal(state):
          return None
        #procuramos a melhor acao seguindo as formulas e pseudocodigos
        #dados nos slides e no livro  
        else:
          melhorValor = float("-inf")
          melhorAcao = 0
          acoesPoss = self.mdp.getPossibleActions(state)
          for acao in acoesPoss:
            transicoes = self.mdp.getTransitionStatesAndProbs(state, acao)
            valor = 0
            for trans in transicoes:
              valor += trans[1]*(self.mdp.getReward(state, acao, trans[0]) + self.discount * self.values[trans[0]])
            if valor > melhorValor:
              melhorAcao = acao
              melhorValor = valor
        return melhorAcao

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
