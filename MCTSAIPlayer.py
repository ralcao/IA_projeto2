import random
from Player import Player
from MCTSNode import Node

class MCTSAIPlayer(Player):
    def __init__(self, piece, max_iterations=1000):
        super().__init__(piece)
        #a peça do nosso agente (1 ou 2)
        self.piece = piece

        #a peça do adversário
        self.opponent = 1 if piece == 2 else 2

        #o numero de vezes que vamos simular jogos antes de decidir
        self.max_iterations = max_iterations


    def get_move(self, board):
        print("\n--- O MCTS ESTÁ A PENSAR ---")
        #criar o ponto de partida que é a raiz da nossa arvore
        #usamos o board.copy pra nao tocar no jogo real
        root = Node(state = board.copy(), action = None)

        #criar o ciclo principal do MCTS
        for i in range (self.max_iterations):
            if i % 200 == 0:
                print(f"A processar iteração {i}...")
            #selecionar o melhor caminho e expandir o novo nó
            node, next_piece_to_play = self._select_and_expand(root)

            #simular um jogo aleatorio a partir desse novo nó
            reward = self._simulate(node.state, next_piece_to_play)

            #atualizar as estatísticas desdo nó ate a raiz
            self._backpropagate(node, reward)

        #tomada de decisão final
        #dps das 1000 iterações escolhemos o nó com melhor ucb
        #passamos c = 0 pois queremos apenas a com mais vitorias nao queremos explorar
        best_node = root.best_child(c=0)
        print(f"--- MCTS DECIDIU: Coluna {best_node.action} ---")

        return best_node.action

    #FUNCOES AUXILIARES - 4 FASES

    def _select_and_expand(self, node):
        #descer na arvore usando o ucb, se ecnontrarmos um nó com jogadas por testar, expandimo-lo
        current_piece = self.piece

        #enquanto o jogo não estiver acabado neste nó
        while not (node.state.check_winner(1) or node.state.check_winner(2) or node.state.is_board_full()):

            #expansao- se ha jogadas que ainda nao tentamos aqui
            if not node.is_fully_expanded():
                #escolhemos uma das jogadas "virgens" à sorte
                action = random.choice(node.untried_moves)
                node.untried_moves.remove(action)

                #criamos um tabuleiro virtual para criar a jogada
                new_state = node.state.copy()
                new_state.drop_piece(action, current_piece)

                #criamos o novo nó e adicionamos com filho do atual
                child = Node (state=new_state, parent = node, action = action)
                node.children.append(child)

                return child, (3 - current_piece)

            #ja usamos tudo deste nó, usamos o ucb para descer para o melhor filho
            else:
                node = node.best_child()
                current_piece = 3 - current_piece #troca o turno a medida que descemos uma arvore

        #se chegou a um estado onde o nó acabou, devolve o nó terminal
        return node, current_piece

    def _simulate(self, state, piece_to_play):
        #joga uma partida completamente à sorte e devolver a recompensa
        sim_state = state.copy()
        current_piece = piece_to_play

        while True:
            #verifica se alguem ganhou
            if sim_state.check_winner(self.piece):
                #o nosso bot venceu, recompensa 1
                return 1.0
            elif sim_state.check_winner(self.opponent):
                #o nosso bot perdeu, recompensa 0
                return 0.0
            elif sim_state.is_board_full():
                #o nosso bot empatou, recompensa 0.5
                return 0.5

            #se ninguem ganhou, escolhe uma coluna à sorte e joga

            valid_moves = sim_state.get_valid_moves()
            action = random.choice (valid_moves)
            sim_state.drop_piece(action, current_piece)

            #passa a vez
            current_piece = 3 - current_piece


    def _backpropagate(self, node, reward):
        """Sobe na árvore a somar as visitas e as vitórias em cada nó."""
        while node is not None:
            node.visits += 1
            node.wins += reward
            # O salto para o nó pai tem de ser SEMPRE a última ação do ciclo!
            node = node.parent


