#Mateus Agostinho dos Anjos
#NUSP 9298191


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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    #Como estamos tratando de busca em profundidade, utilizaremos
    #uma pilha para guardar os nohs da fronteira
    fronteira = util.Stack()
    #Aqui armazenaremos os nohs Explorados (nosExplorados)
    nosExplorados = []

    #Primeiro colocamos na fronteira o noh inicial com o codigo "Stop" para
    #sinalizar a parada. Preenchemos "Stop" e '0' para a fronteira
    #ficar coerente para todos os nohs
    fronteira.push([(problem.getStartState(), "Stop", 0)])

    #Enquanto tivermos nohs na fronteira faremos:
    while not fronteira.isEmpty():
        #Pegamos a coordenada do noh da fronteira mais recente
        #(Busca em profundidade)
        caminho = fronteira.pop()
        coordenada = caminho[len(caminho)-1]
        coordenada = coordenada[0]

        #Verificamos se este noh eh o estado final
        if problem.isGoalState(coordenada):
            #lista de direcoes, que deve ser passada como resposta
            direcoes = []
            #se chegarmos no final teremos que devolver o caminho encontrado
            for x in caminho:
                #Aqui adicionamos a direcao de cada noh do caminho encontrado
                direcoes.append(x[1])
            #devolvemos direcoes[1:] pois nao queremos contar "Stop"
            #como direcao    
            return direcoes[1:]    
        #Se coordenada nao tiver sido explorado ainda, colocamos a coordenada na lista
        #de nohs explorados
        if coordenada not in nosExplorados:
            nosExplorados.append(coordenada)
            #Agora pegaremos o sucessor de coordenada
            for sucessor in problem.getSuccessors(coordenada):
                if sucessor[0] not in nosExplorados:
                    sucessorCaminho = caminho[:]
                    sucessorCaminho.append(sucessor)
                    fronteira.push(sucessorCaminho)    
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    
    #Aqui temos a mudanca entre a busca em profundidade e a busca em largura
    #Para busca em largura, armazenaremos os nohs da fronteira em uma
    #fila, pegando sempre o noh mais superficial, expandindo todo o
    #nivel da arvore.
    fronteira = util.Queue()
    
    #O codigo abaixo eh igual ao codigo documentado em: depthFirstSearch(problem) linha 75
    nosExplorados = []
    fronteira.push([(problem.getStartState(), "Stop", 0)])

    while not fronteira.isEmpty():
        caminho = fronteira.pop()
        coordenada = caminho[len(caminho)-1]
        coordenada = coordenada[0]

        if problem.isGoalState(coordenada):
            direcoes = []
            for x in caminho:
                direcoes.append(x[1])    
            return direcoes[1:]    
        if coordenada not in nosExplorados:
            nosExplorados.append(coordenada)
            for sucessor in problem.getSuccessors(coordenada):
                if sucessor[0] not in nosExplorados:
                    sucessorCaminho = caminho[:]
                    sucessorCaminho.append(sucessor)
                    fronteira.push(sucessorCaminho)    
    return []

def iterativeDeepeningSearch(problem):
    """
    Start with depth = 0.
    Search the deepest nodes in the search tree first up to a given depth.
    If solution not found, increment depth limit and start over.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    """
    
    #Como estamos tratando de busca em profundidade, utilizaremos
    #uma pilha para guardar os nohs da fronteira e uma pilha para
    #guardar a profundidade dos nohs
    #Estas estruturas nao precisam ser reiniciadas a cada mudanca de "depth",
    #pois quando incrementamos "depth" dentro da busca, fronteira e profundidade
    #estarao vazias (linha 206(profundidade acompanha fronteira))
    fronteira = util.Stack()
    profundidade = util.Stack()

    #Aqui temos depth(profundidade) = 0 que caracteriza a busca em 
    #profundidade iterativa
    depth = 0


    #Como sabemos que existe a comida, sabemos que existe um caminho, por isso
    #while True pode ser colocado aqui.
    #Entretando a busca ids eh utilizada se quisermos limitar a profundidade,
    #a fim de evitar loops infinitos, portanto while depth < N (N sendo
    #a profundidade maxima a ser explorada) seria mais indicado
    #caso N fosse fornecido
    while True:
        #Dicionario utilizado para implementar a modificacao da busca ids
        #a fim de torna-la otima. custos["coordenadaX"] = menor custo para
        #chegar a X
        custos = {}
        #Custo do estado inicial eh zero
        custos[problem.getStartState()] = 0
        #Devemos ter uma lista nova de nosExplorados para cada profundidade
        nosExplorados = []
        #Adicionamos a profundidade ao noh da fronteira
        fronteira.push([(problem.getStartState(), "Stop", 0)])
        profundidade.push(0)
        #Enquanto tivermos nohs na fronteira faremos:
        while not fronteira.isEmpty():
            #Pegamos a coordenada do noh da fronteira mais recente
            #(Busca em profundidade)
            caminho = fronteira.pop()
            coordenada = caminho[len(caminho)-1]
            #Pegamos a profundidade deste Noh
            profundidadeNoh = profundidade.pop()
            coordenada = coordenada[0]


            #Verificamos se este noh eh o estado final
            if problem.isGoalState(coordenada):
                #lista de direcoes, que deve ser passada como resposta
                direcoes = []
                #se chegarmos no final teremos que devolver o caminho encontrado
                for x in caminho:
                    #Aqui adicionamos a direcao de cada noh do caminho encontrado
                    direcoes.append(x[1])
                #devolvemos direcoes[1:] pois nao queremos contar "Stop"
                #como direcao    
                return direcoes[1:]    
            #Se coordenada nao tiver sido explorado ainda, colocamos a coordenada na lista
            #de nohs explorados
            if coordenada not in nosExplorados:
                nosExplorados.append(coordenada)
                #Se a profundidade do noh for menor que depth, podemos
                #expandir seus filhos, caso contrario fingimos que ele nao possui
                #filhos, limitando a profundidade
            if profundidadeNoh < depth:
                for sucessor in problem.getSuccessors(coordenada):
                    #O estado de sucessor[0] ainda nao foi explorado, por isso
                    #o colocamos na fronteira diretamente 
                    if sucessor[0] not in nosExplorados:
                        sucessorCaminho = caminho[:]
                        sucessorCaminho.append(sucessor)
                        fronteira.push(sucessorCaminho)
                        profundidade.push(profundidadeNoh+1)
                        custos[sucessor[0]] = profundidadeNoh + 1
                    #O estado de sucessor[0] ja foi explorado, aqui implementaremos
                    #a modificacao da ids, para torna-la otima.    
                    else:
                        #custos[sucessor[0]] eh o menor custo, ate o momento, para
                        #encontrar o estado sucessor[0]. profundidadeNoh + 1 eh o custo
                        #para chegar a sucessor[0] no caminho que esta sendo explorado
                        #no momento. (Isto soh eh valido, pois o custo de todas as acoes
                        #do PacMan eh igual a 1. Caso contrario teriamos que percorrer
                        #o caminho ate esse noh e calcular seu custo).
                        if custos[sucessor[0]] > profundidadeNoh + 1:
                            #Ao executar o bloco de codigo a seguir, garantimos que
                            #o custo de chegar ao estado sucessor[0] no caminho explorado
                            #no momento eh menor do que qualquer custo de chegar neste
                            #mesmo estado por outros caminhos explorados ate aqui. Portanto, 
                            #este eh um caminho a ser explorado. (tornando a busca otima)
                            sucessorCaminho = caminho[:]
                            sucessorCaminho.append(sucessor)
                            fronteira.push(sucessorCaminho)
                            profundidade.push(profundidadeNoh+1)
                            #Atualizamos o novo custo de se chegar ao estado sucessor[0]
                            custos[sucessor[0]] = profundidadeNoh + 1
        depth += 1
    return []



def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    
    #Primeiro devemos definir uma funcao de custo a ser passada para a
    #fila de prioridades. Para essa funcao apenas definiremos o custo do
    #caminho ate o proprio noh, uma vez que o esse modo de busca eh de custo uniforme
    custo = lambda funcao: problem.getCostOfActions([x[1] for x in funcao])
    fronteira = util.PriorityQueueWithFunction(custo)

    #O codigo abaixo eh igual ao codigo documentado em: depthFirstSearch(problem) linha 75
    nosExplorados = []
    fronteira.push([(problem.getStartState(), "Stop", 0)])

    while not fronteira.isEmpty():
        caminho = fronteira.pop()
        coordenada = caminho[len(caminho)-1]
        coordenada = coordenada[0]

        if problem.isGoalState(coordenada):
            direcoes = []
            for x in caminho:
                direcoes.append(x[1])    
            return direcoes[1:]    
        if coordenada not in nosExplorados:
            nosExplorados.append(coordenada)
            for sucessor in problem.getSuccessors(coordenada):
                if sucessor[0] not in nosExplorados:
                    sucessorCaminho = caminho[:]
                    sucessorCaminho.append(sucessor)
                    fronteira.push(sucessorCaminho)    
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    #Para a busca A* devemos definir uma funcao de custo para ser passada
    #para a fila de prioridades. Essa funcao levara em conta o custo do caminho
    #ate o noh somado a sua heuristica (caracterizando a busca A*)
    custo = lambda funcao: problem.getCostOfActions([x[1] for x in funcao][1:]) + heuristic(funcao[len(funcao)-1][0], problem)
    fronteira = util.PriorityQueueWithFunction(custo)

    #O codigo abaixo eh igual ao codigo documentado em: depthFirstSearch(problem) linha 75
    nosExplorados = []
    fronteira.push([(problem.getStartState(), "Stop", 0)])

    while not fronteira.isEmpty():
        caminho = fronteira.pop()
        coordenada = caminho[len(caminho)-1]
        coordenada = coordenada[0]

        if problem.isGoalState(coordenada):
            direcoes = []
            for x in caminho:
                direcoes.append(x[1])    
            return direcoes[1:]    
        if coordenada not in nosExplorados:
            nosExplorados.append(coordenada)
            for sucessor in problem.getSuccessors(coordenada):
                if sucessor[0] not in nosExplorados:
                    sucessorCaminho = caminho[:]
                    sucessorCaminho.append(sucessor)
                    fronteira.push(sucessorCaminho)    
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch