"""
Script de recolha de dados para a tabela resultados.xlsx
Corre os jogos e imprime os valores prontos a copiar para o Excel.
"""
import time
from Connect4Board import Connect4Board
from MinimaxPlayer import MinimaxAIPlayer
from RandomPlayer import RandomAIPlayer
# Descomenta quando o teu colega terminar o MCTS:
from MCTSAIPlayer import MCTSAIPlayer


def play_game(p1, p2, rows=6, cols=7, n_connect=4):
    """Simula um jogo completo sem GUI. Devolve (vencedor, duracao_segundos)."""
    board = Connect4Board(rows, cols, n_connect)
    players = [p1, p2]
    turn = 0
    start = time.time()
    while True:
        current = players[turn]
        col = current.get_move(board)
        board.drop_piece(col, current.piece)
        if board.check_winner(current.piece):
            return current.piece, round(time.time() - start, 2)
        if board.is_board_full():
            return 0, round(time.time() - start, 2)
        turn = (turn + 1) % 2


def run_comparison(label, make_p1, make_p2, n_games=50):
    """Corre n_games jogos e imprime os resultados formatados."""
    print(f"\n{'='*60}")
    print(f"  {label}  ({n_games} jogos)")
    print(f"{'='*60}")

    wins_p1, wins_p2, draws = 0, 0, 0
    durations = []

    for i in range(n_games):
        p1 = make_p1()
        p2 = make_p2()
        winner, duration = play_game(p1, p2)
        durations.append(duration)
        if winner == 1:
            wins_p1 += 1
        elif winner == 2:
            wins_p2 += 1
        else:
            draws += 1

        # Progresso
        if (i + 1) % 10 == 0:
            print(f"  ... {i+1}/{n_games} jogos concluidos")

    taxa_p1 = f"{wins_p1/n_games*100:.0f}%"
    taxa_p2 = f"{wins_p2/n_games*100:.0f}%"
    media   = round(sum(durations) / len(durations), 1)
    maximo  = max(durations)
    minimo  = min(durations)

    print(f"\n  Nº Jogos               : {n_games}")
    print(f"  Vitórias Jogador 1     : {wins_p1}")
    print(f"  Vitórias Jogador 2     : {wins_p2}")
    print(f"  Empates                : {draws}")
    print(f"  Taxa Vitórias P1       : {taxa_p1}")
    print(f"  Taxa Vitórias P2       : {taxa_p2}")
    print(f"  Duração Média (segundos): {media}s")
    print(f"  Duração Máxima          : {maximo}s")
    print(f"  Duração Mínima          : {minimo}s")

    return {
        "label": label, "n": n_games,
        "w1": wins_p1, "w2": wins_p2, "draws": draws,
        "t1": taxa_p1, "t2": taxa_p2,
        "media": media, "max": maximo, "min": minimo
    }


# ── 1. Minimax vs Aleatório ───────────────────────────────────────────────────
#run_comparison(
    label="Minimax vs Aleatório",
    make_p1=lambda: MinimaxAIPlayer(piece=1, max_depth=5),
    make_p2=lambda: RandomAIPlayer(piece=2),
    n_games=25
#)

# ── 2. MCTS vs Aleatório (descomenta quando o MCTS estiver pronto) ────────────
# run_comparison(
#     label="MCTS vs Aleatório",
#     make_p1=lambda: MCTSAIPlayer(piece=1, max_iterations=1000),
#     make_p2=lambda: RandomAIPlayer(piece=2),
#     n_games=50
# )

# ── 3. Minimax vs MCTS — 3 combinações (descomenta quando o MCTS estiver pronto) ──
#COMBINAÇÃO 1 — tempo curto (ex: depth=3, iterations=300)#
#run_comparison(
 #    label="1ª comb — Minimax(depth=3) vs MCTS(iter=300)",
  #   make_p1=lambda: MinimaxAIPlayer(piece=1, max_depth=3),
   #  make_p2=lambda: MCTSAIPlayer(piece=2, max_iterations=300),
    # n_games=50
#)

#COMBINAÇÃO 2 — tempo médio (ex: depth=5, iterations=1000)
run_comparison(
     label="2ª comb — Minimax(depth=4) vs MCTS(iter=1000)",
     make_p1=lambda: MinimaxAIPlayer(piece=1, max_depth=4),
     make_p2=lambda: MCTSAIPlayer(piece=2, max_iterations=1000),
     n_games=50
)

# COMBINAÇÃO 3 — tempo longo (ex: depth=7, iterations=3000)
# run_comparison(
#     label="3ª comb — Minimax(depth=7) vs MCTS(iter=3000)",
#     make_p1=lambda: MinimaxAIPlayer(piece=1, max_depth=7),
#     make_p2=lambda: MCTSAIPlayer(piece=2, max_iterations=3000),
#     n_games=50
# )

print("\n\nFim. Copia os valores acima para o resultados.xlsx.")
