import math

class Node:
    def __init__(self, state, parent=None, action=None):
        #Dados do nó
        self.state = state #o estado do tabuleiro do jogo nesse exato momento
        self.parent = parent #o nó pai respetivo (de onde "viemos")
        self.action = action #a jogada (coluna) que o jogador fez para chegar a este contexto
        self.children = [] #uma lista que vai guardar as jogadas seguintes (nós filhos)

        #Estatísticas para a fórmula UCB
        self.wins = 0 #quantas vitórias fez a simulação que passou por aqui
        self.visits = 0 #quantas vezes o algoritmo passou por este nó

        #Controlo de "expansão"
        #serve para guardar as colunas válidas no momento que o nó é criado
        #isto ajuda a saber que jogadas faltam testar

        self.untried_moves = list(state.get_valid_moves())#

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0
        #se a lista de jogadas não feitas estiver vazia, já tentamos tudo
        #ou seja, verificamos se todas as jogadas possíveis já foram exploradas e transformadas em filhos

    def ucb(self, c=1.414):
        if self.visits==0:
            return float('inf')
        #daria erro com 0 visitas, precavemos esse erro da forma acima

        exploitation = self.wins / self.visits
        #o termo de exploitation, qual a nossa taxa de sucesso na jogada?

        exploration = c * math.sqrt(math.log(self.parent.visits) / self.visits)
        #o termo de exploration, há quanto tempo não visitamos o pai nesta jogada, comparado com o total?

        return exploitation + exploration
        #calculamos a formula ucb para o nó

    def best_child(self, c=1.414):
        return max(self.children, key=lambda child: child.ucb(c))
        #percorrer a lista e encontrar o que devolver maior numero da funcao ucb



