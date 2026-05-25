from Player import Player

class MinimaxAIPlayer(Player):
    def __init__(self, piece, max_depth=5):
        super().__init__(piece)
        self.max_depth = max_depth
        self.opponent_piece = 2 if piece == 1 else 1

    def get_move(self, board):
        #print(f"\n--- MINIMAX (Profundidade {self.max_depth}) A PENSAR ---")

        # O Minimax devolve a pontuação esperada e a coluna
        best_score, col = self.minimax(board, self.max_depth, float('-inf'), float('inf'), True)

        # Traduzir o score para algo humano perceber no terminal
        if best_score > 9000:
            estado = "ENCONTREI VITÓRIA GARANTIDA!"
        elif best_score < -9000:
            estado = "ESTOU EM PÂNICO (Vou perder...)"
        elif best_score > 50:
            estado = "Estou ao ataque"
        elif best_score < -30:
            estado = "Estou a defender/bloquear"
        else:
            estado = "A desenvolver jogo no centro"

        #print(f"--- MINIMAX DECIDIU: Coluna {col} | Score: {best_score} ({estado}) ---")
        return col


    def minimax(self, board, depth, alpha, beta, maximizing):
        # Verificar estados terminais antes de gerar novos movimentos
        if board.check_winner(self.piece):
            return (10000 + depth, None)
        if board.check_winner(self.opponent_piece):
            return (-10000 - depth, None)
        if board.is_board_full():
            return (0, None)
        if depth == 0:
            # Chamada com os dois argumentos exigidos pelo enunciado V2.0
            return (self.evaluate_board(board, self.piece), None)

        # Ordenar colunas do centro para os extremos melhora a poda alpha-beta
        center = board.cols // 2
        valid_moves = sorted(board.get_valid_moves(), key=lambda c: abs(c - center))
        best_col = valid_moves[0]

        if maximizing:
            max_score = float('-inf')
            for col in valid_moves:
                new_board = board.copy()
                new_board.drop_piece(col, self.piece)
                score, _ = self.minimax(new_board, depth - 1, alpha, beta, False)
                if score > max_score:
                    max_score = score
                    best_col = col
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_score, best_col
        else:
            min_score = float('inf')
            for col in valid_moves:
                new_board = board.copy()
                new_board.drop_piece(col, self.opponent_piece)
                score, _ = self.minimax(new_board, depth - 1, alpha, beta, True)
                if score < min_score:
                    min_score = score
                    best_col = col
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score, best_col

    def evaluate_board(self, board, player):
        # Assinatura corrigida para V2.0: recebe player como argumento
        # Isto permite que a função seja chamada externamente para avaliar
        # o tabuleiro do ponto de vista de qualquer jogador
        opponent = 2 if player == 1 else 1
        score = 0
        n = board.n_connect

        # Bonus por pecas na coluna central
        center_col = board.cols // 2
        center_column = [int(board.grid[r][center_col]) for r in range(board.rows)]
        score += center_column.count(player) * 3

        # Avaliar todas as janelas de tamanho n em cada direcao
        for r in range(board.rows):
            for c in range(board.cols - n + 1):
                window = [int(board.grid[r][c + i]) for i in range(n)]
                score += self.score_window(window, player, opponent)

        for c in range(board.cols):
            for r in range(board.rows - n + 1):
                window = [int(board.grid[r + i][c]) for i in range(n)]
                score += self.score_window(window, player, opponent)

        for r in range(n - 1, board.rows):
            for c in range(board.cols - n + 1):
                window = [int(board.grid[r - i][c + i]) for i in range(n)]
                score += self.score_window(window, player, opponent)

        for r in range(board.rows - n + 1):
            for c in range(board.cols - n + 1):
                window = [int(board.grid[r + i][c + i]) for i in range(n)]
                score += self.score_window(window, player, opponent)

        return score

    def score_window(self, window, player, opponent):
        n = len(window)
        player_count = window.count(player)
        empty_count = window.count(0)
        opponent_count = window.count(opponent)
        score = 0

        if player_count == n - 1 and empty_count == 1:
            score += 5
        elif player_count == n - 2 and opponent_count == 0:
            score += 2

        if opponent_count == n - 1 and empty_count == 1:
            score -= 4

        return score
