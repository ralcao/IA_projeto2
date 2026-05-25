import time
from Connect4Board import Connect4Board
from MinimaxPlayer import MinimaxAIPlayer
from RandomPlayer import RandomAIPlayer

def imprimir_tabuleiro(board):
    """Função auxiliar para desenhar o tabuleiro no terminal"""
    print("\n  0 1 2 3 4 5 6")
    print(" ---------------")
    for r in range(board.rows):
        linha = "|"
        for c in range(board.cols):
            peca = board.grid[r][c]
            if peca == 1: linha += " X" # Peça 1
            elif peca == 2: linha += " O" # Peça 2
            else: linha += " ."
        print(linha + " |")
    print(" ---------------\n")

def main():
    board = Connect4Board()
    # Minimax é o X (Peça 1), Aleatório é o O (Peça 2)
    p1 = MinimaxAIPlayer(piece=1, max_depth=4)
    p2 = RandomAIPlayer(piece=2)

    players = {1: p1, 2: p2}
    turn = 1

    print("=== INÍCIO DO JOGO: MINIMAX (X) vs ALEATÓRIO (O) ===")
    imprimir_tabuleiro(board)

    while True:
        current_player = players[turn]

        if isinstance(current_player, RandomAIPlayer):
            print(f"\nTurno do Aleatório (Peça {turn})...")

        # Pede a jogada ao bot
        col = current_player.get_move(board)
        board.drop_piece(col, current_player.piece)

        # Imprime o estado atual
        imprimir_tabuleiro(board)
        time.sleep(0.5) # Pausa de meio segundo para conseguires ler

        if board.check_winner(current_player.piece):
            print(f"🏆 JOGADOR {current_player.piece} VENCEU! 🏆")
            break
        if board.is_board_full():
            print("🤝 EMPATE! O tabuleiro está cheio.")
            break

        turn = 3 - turn # Troca o turno (1 vira 2, 2 vira 1)

if __name__ == "__main__":
    main()