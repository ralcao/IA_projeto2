"""
Testes ao MinimaxAIPlayer sem necessidade de pygame.
Simula o loop de jogo directamente com Connect4Board.
"""
from Connect4Board import Connect4Board
from MinimaxPlayer import MinimaxAIPlayer
from RandomPlayer import RandomAIPlayer


def play_game(p1, p2):
    """Simula um jogo completo sem GUI. Devolve (vencedor, nr_jogadas)."""
    board = Connect4Board()
    players = [p1, p2]
    turn = 0
    moves = 0
    while True:
        current = players[turn]
        col = current.get_move(board)
        assert col in board.get_valid_moves(), f"Jogada invalida: coluna {col}"
        board.drop_piece(col, current.piece)
        moves += 1
        if board.check_winner(current.piece):
            return current.piece, moves
        if board.is_board_full():
            return 0, moves
        turn = (turn + 1) % 2


# ── Teste 1: assinatura evaluate_board(board, player) ────────────────────────
board = Connect4Board()
p1 = MinimaxAIPlayer(piece=1, max_depth=4)

s1 = p1.evaluate_board(board, 1)
s2 = p1.evaluate_board(board, 2)
assert isinstance(s1, (int, float)), "evaluate_board deve devolver um numero"
assert isinstance(s2, (int, float)), "evaluate_board deve devolver um numero"
print(f"[OK] evaluate_board(board, 1) = {s1}")
print(f"[OK] evaluate_board(board, 2) = {s2}")

# ── Teste 2: get_move devolve coluna valida ───────────────────────────────────
move = p1.get_move(board)
assert move in board.get_valid_moves(), f"get_move devolveu coluna invalida: {move}"
print(f"[OK] get_move() = coluna {move} (valida)")

# ── Teste 3: Minimax vs Aleatorio (10 jogos) ─────────────────────────────────
wins, losses, draws = 0, 0, 0
total_moves = []

for _ in range(10):
    winner, n = play_game(MinimaxAIPlayer(piece=1, max_depth=4), RandomAIPlayer(piece=2))
    total_moves.append(n)
    if winner == 1: wins += 1
    elif winner == 2: losses += 1
    else: draws += 1

print(f"\n[OK] 10 jogos Minimax(P1) vs Aleatorio(P2):")
print(f"     Vitorias Minimax : {wins}")
print(f"     Vitorias Aleatorio: {losses}")
print(f"     Empates          : {draws}")
print(f"     Jogadas media    : {sum(total_moves)/len(total_moves):.1f}")
print(f"     Jogadas min/max  : {min(total_moves)} / {max(total_moves)}")

assert wins >= 8, f"Minimax devia ganhar >80% contra aleatorio, ganhou {wins}/10"
print("\n[TODOS OS TESTES PASSARAM]")
