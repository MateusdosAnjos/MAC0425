#Nome: Mateus Agostinho dos Anjos
#NUSP: 9298191

# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    answerDiscount = 0.9
    #Tirando o noise nosso agente tem 100% de chance de executar a acao
    #proposta, portanto ele consegue atravessar a ponte
    answerNoise = 0.0
    return answerDiscount, answerNoise

def question3a():
    #Para este caso, devemos considerar um alto desconto para o agente #escolher a saida mais proxima, tomando cuidado para nao exagerar,
    #pois o agente poderia escolher pular no precipicio caso fosse
    #muito grande(valores de answerDiscount muito pequenos). 
    #Nao devemos bonifica-lo por viver para evitar que o agente tome o #caminho mais longo
    #Colocamos um noise baixo, para que o agente considere o risco de andar
    #proximo ao precipicio
    answerDiscount = 0.3
    answerNoise = 0.01
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    #Para este caso, devemos considerar um alto desconto para o agente #escolher a saida mais proxima, tomando cuidado para nao exagerar.
    #Nao devemos bonifica-lo por viver para evitar que o agente tome o #caminho mais longo.
    #Colocamos um noise maior que o do exercicio anterior, para que o agente #nao aceite o risco de andar proximo ao precipicio, assim tome o caminho
    #mais longo para a saida mais proxima
    answerDiscount = 0.3
    answerNoise = 0.05
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    #Para este caso, devemos considerar um desconto moderado para o agente #escolher a saida mais distante pelo menor caminho.
    #Colocamos um noise pequeno, para que o agente aceite o risco de andar #proximo ao precipicio
    answerDiscount = 0.6
    answerNoise = 0.01
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    #Para este caso, devemos considerar um desconto pequeno (alto valor de
    #answerDiscount) para o agente escolher a saida mais distante(pois ela #vale 10).
    #Aumentamos o noise, para que o agente nao aceite o risco de andar #proximo ao precipicio
    answerDiscount = 0.9
    answerNoise = 0.1
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    #Para evitar as saidas nao podemos descontar nada do reward
    #assim o agente tentara manter o estado em que comecou
    answerDiscount = 1
    answerNoise = 0.01
    answerLivingReward = 1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question6():
    #50 iteracoes sao muito poucas para que o agente
    #encontre a politica otima, portanto devolvemos
    # 'NOT POSSIBLE'
    answerEpsilon = None
    answerLearningRate = None
    return 'NOT POSSIBLE'
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print 'Answers to analysis questions:'
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print '  Question %s:\t%s' % (q, str(response))
