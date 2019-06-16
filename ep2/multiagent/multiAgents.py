#Nome: Mateus Agostinho dos Anjos
#NUSP: 9298191

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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #Um modo de jogar eh evitar a todo custo os fantasmas e buscar comer
        #as comidas que estiverem mais perto do PACMAN.
        #comecamos a avaliacao a partir do score do estado analisado
        aval = successorGameState.getScore()

        #Primeiro o pacman evitar os fantasmas a todo custo.
        #Faremos isso atribuindo uma melhor avaliacao para
        #os movimentos que deixarem os fantasmas distantes de
        #um certo "raio" do pacman
        #Um numero grande como a menor distancia
        menorDistF = 9000000042
        for fantasmas in newGhostStates:
          distFantasma = manhattanDistance(newPos, fantasmas.getPosition())
          if menorDistF > distFantasma:
            menorDistF = distFantasma
        #Se o fantasma mais proximo estiver a um raio de 2 do PACMAN
        #o score recebera um desconto (o maior desconto, pois este eh
        #um caso de possivel derrota)    
        if menorDistF <= 2:
          aval -= 40      
        
        #Aqui em posComidas temos a posicao das comidas do jogo,
        #transformada em lista com .asList()
        posComidas = (currentGameState.getFood()).asList()
        #Calcularemos a soma das distancias das comidas mais proximas
        #para o estado atual do pacman no jogo
        distanciaComidasAtuais = []
        for comida in posComidas:
          distanciaComidasAtuais.append(util.manhattanDistance(comida, currentGameState.getPacmanPosition()))
        comidasAtuais = sum(distanciaComidasAtuais)

        #Aqui calculamos a soma das distancias das comidas mais proximas para
        #o estado apos o movimento que esta sendo analisado
        distanciaComidas = []
        for comida in newFood.asList():
          distanciaComidas.append(util.manhattanDistance(comida, newPos))
        comidasProximas = sum(distanciaComidas)

        if comidasProximas == 0:
          comidasProximas = 1
        if comidasAtuais == 0:
          comidasAtuais = 1  
        #Agora veremos se, apos o movimento do PACMAN, ele estara mais proximo
        #de um aglomerado de comidas, utilizamos a dica do enunciado em comparar
        #o inverso.
        if 1/comidasProximas > 1/comidasAtuais:
          #Aqui poderamos o quanto melhor seria esta posicao analisada
          aval += (1/comidasAtuais - 1/comidasProximas) * 2
        else:
          aval -= 20

        #Faremos agora uma analise parecida com a anterior, porem para
        #apenas um (1) comida
        if len(distanciaComidasAtuais) > 0:
          comidaMaisProximaAtual = min(distanciaComidasAtuais)
        else:
          comidaMaisProximaAtual = 1
        if len(distanciaComidas) > 0:
          comidaMaisProxima = min(distanciaComidas)
        else:
          comidaMaisProxima = 1  
        if comidaMaisProxima < comidaMaisProximaAtual:
          aval += (comidaMaisProximaAtual - comidaMaisProxima) * 2
        else:
          aval -= 20             
        return aval

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
        melhorPlacar, melhorMovimento = self.MAX(gameState, self.depth)
        return melhorMovimento

    #Remove o STOP da lista de acoes. Dito no enunciado:
    #"Para aumentar a profundidade da busca, retire a acao Directions.STOP da lista de acoes
    #possiveis do Pac-Man"
    def removeStop(self, movimentosValidos):
        stop = Directions.STOP
        if stop in movimentosValidos:
          movimentosValidos.remove(stop)    

    #Seguindo o modelo do livro com a alteracao, criamos:    
    def MAX(self, gameState, profundidade):
        #Aqui temos os casos em que o pacman nao precisa se mover
        if profundidade == 0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "noMove"
        #Veremos, dentre os movimentos possiveis, qual o melhor para MAX
        movimentos = gameState.getLegalActions()
        #retiramos STOP dos movimentos
        self.removeStop(movimentos)
        palacares = []
        #Aqui analisamos os possiveis movimentos de min, para escolhermos o movimento
        #que agradaria mais a MAX
        for movimento in movimentos:
          palacares.append([self.min(gameState.generateSuccessor(self.index, movimento), 1, profundidade)])
        #Melhor palacar para MAX  
        melhorPlacar = max(palacares)
        #Pegamos qual movimento que gera o melhor placar para MAX
        for i in range(len(palacares)):
          if palacares[i] == melhorPlacar:
            melhorInd = i    
        return melhorPlacar, movimentos[melhorInd]

    def min(self, gameState, agente, profundidade):  
        if profundidade == 0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "noMove"
        #Pegamos os movimentos do fantasma (agente >= 1)
        movimentos = gameState.getLegalActions(agente)
        #retiramos STOP dos movimentos
        self.removeStop(movimentos)
        placares = []
        #Verificamos se ainda ha fantasmas a serem analisados (recursao)
        if(agente != gameState.getNumAgents() - 1):
          #Aqui colocamos a modificacao para analizar mais de 1 fantasma (recursao)
          for movimento in movimentos:
            placares.append([self.min(gameState.generateSuccessor(agente, movimento), agente + 1, profundidade)])
        #Chamada do MAX
        else:
          for movimento in movimentos:
            placares.append([self.MAX(gameState.generateSuccessor(agente, movimento), (profundidade - 1))])
        #Pior placar para MAX(PACMAN)
        menorPlacar = min(placares)
        for i in range(len(placares)):
          if placares[i] == menorPlacar:
            piorInd = i
        return menorPlacar, movimentos[piorInd]        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
      """
      Returns the minimax action using self.depth and self.evaluationFunction
      """
      #Apenas para facilitar o entendimento, chamamos PACMAN = 0          
      PACMAN = 0
      #Lembrando que, como no minimax, aqui ja guardamos o "melhorMovimento"
      #(action with value v) dentro de max_value.
      #Implementando o que foi passado no enunciado temos:
      def max_value(state, profundidade, alpha, beta):
        #casos base
        if state.isWin() or state.isLose():
          return state.getScore()
        #pegamos a lista de movimentos validos para o agente PACMAN  
        movimentos = state.getLegalActions(PACMAN)
        #Aqui v eh o valor
        v = float("-inf")
        aval = v
        melhorMovimento = Directions.STOP
        #do enunciado: "for each sucessor of state:"
        for movimento in movimentos:
          aval = min_value(state.generateSuccessor(PACMAN, movimento), profundidade, 1, alpha, beta)
          #nesta parte estamos fazendo o v = max(v, value(sucessor, alpha, beta))
          if aval > v:
            v = aval
            melhorMovimento = movimento
          #aqui fazemos a parte do if v > beta return v
          if v > beta:
            return v
          #parte do alpha = max(alpha, v)    
          alpha = max(alpha, v)
        if profundidade == 0:
          return melhorMovimento
        else:
          return v
      #Implementando o que foi passado no enunciado temos:
      def min_value(state, profundidade, fantasma, alpha, beta):
        #casos base
        if state.isLose() or state.isWin():
          return state.getScore()
        #pegamos o agente circularmente  
        agente = (fantasma + 1)%state.getNumAgents()
        #lista de movimentos do fantasma
        movimentos = state.getLegalActions(fantasma)
        #Aqui v eh o valor
        v = float("inf")
        aval = v
        #do enunciado: "for each sucessor of state:"
        for movimento in movimentos:
          #Se o agente eh o PACMAN devemos maximizar
          if agente == PACMAN:
            if profundidade == self.depth - 1:
              aval = self.evaluationFunction(state.generateSuccessor(fantasma, movimento))
            else:
              aval = max_value(state.generateSuccessor(fantasma, movimento), profundidade + 1, alpha, beta)
          #Aqui o agente eh fantasma, portanto devemos minimizar    
          else:
            aval = min_value(state.generateSuccessor(fantasma, movimento), profundidade, agente, alpha, beta)
          #pegamos o menor valor  
          if aval < v:
            v = aval
          #parte do if v < alpha return v
          if v < alpha:
            return v
          #parte do beta = min(beta, v)  
          beta = min(beta, v)
        return v
      #Chamada da funcao max_value para o comeco do algoritmo alphabeta
      return max_value(gameState, 0, float("-inf"), float("inf"))

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
      #funcao getActionMod faz o trabalho, pegamos a posicao [1] da lista, pois
      #ela contem o movimento. (posicao [0] contem o valor de avaliacao v)
      return self.getActionMod(gameState, self.depth, 0)[1]

    def getActionMod(self, gameState, profundidade, agente):
      PACMAN = 0
      #casos base
      if profundidade == 0 or gameState.isWin() or gameState.isLose():
          resultAval = self.evaluationFunction(gameState)
          return (resultAval, 'noMove')
      else:
          #se ja analisamos todos os agentes, devemos subir um nivel da arvore
          if agente == gameState.getNumAgents() - 1:
              profundidade -= 1
          #se o agente for o pacman o valor inicial de v sera -inf    
          if agente == PACMAN:
              v = float("-inf")
          else:
              v = 0
          #por enquanto o melhor movimento eh nao se mover    
          melhorMovimento = 'noMove'
          #incrementamos o agente para o proximo, circularmente
          proxAgente = (agente + 1) % gameState.getNumAgents()
          #geramos os movimentos para o agente atual
          movimentos = gameState.getLegalActions(agente)
          #para a lista de movimentos do agente atual faremos:
          for movimento in movimentos:
              #calculamos sua avaliacao
              avaliacao = self.getActionMod(gameState.generateSuccessor(agente, movimento), profundidade, proxAgente)
              #se o agente for o pacman devemos pegar o movimento da maior avaliacao v
              if agente == PACMAN:
                  if avaliacao[0] > v:
                      v = avaliacao[0]
                      melhorMovimento = movimento
              #se o agente for fantasma, devemos calcular a probabilidade para o valor v (caracteristica do Expectimax)
              else:
                  v += 1.0/len(movimentos) * avaliacao[0]
                  melhorMovimento = movimento
      return (v, melhorMovimento)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    #Se ganhar mais rapido, melhor. Portanto devemos atribuir a vitoria um valor
    #extremamente grande
    if currentGameState.isWin():
      return float("inf")
    #Perder eh ruim, a menos que nao haja escapatoria  
    if currentGameState.isLose():
        return  float("-inf")   
    aval = scoreEvaluationFunction(currentGameState)
    #pegamos as posicoes das comidas
    posComidas = (currentGameState.getFood()).asList()
    menorDistComida = float("inf")
    #calculamos a menor distancia ate a comida
    for pos in posComidas:
        distanciaComida = util.manhattanDistance(pos, currentGameState.getPacmanPosition())
        if distanciaComida < menorDistComida:
            menorDistComida = distanciaComida
    #Quanto mais proximo a comida, melhor        
    aval -= menorDistComida * 2
    #Quanto menos comidas, melhor
    aval -= len(posComidas) * 4  
    
    #Calculando avaliacoes para os fantasmas
    fantasmas = currentGameState.getNumAgents() - 1
    #PACMAN eh o agente 0, portanto i = 1 eh o primeiro fantasma
    i = 1
    #menor distancia para o fantasma, iniciamos com +infinito
    menorDistF = float("inf")
    #veremos qual o fantasma mais proximo
    while i <= fantasmas:
        proxDist = util.manhattanDistance(currentGameState.getPacmanPosition(), currentGameState.getGhostPosition(i))
        menorDistF = min(menorDistF, proxDist)
        i += 1    
    if menorDistF <= 2:
      aval -= menorDistF * 2
    return aval    

# Abbreviation
better = betterEvaluationFunction

