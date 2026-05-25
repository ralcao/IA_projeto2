import time
from RandomPlayer import RandomAIPlayer
from MCTSAIPlayer import MCTSAIPlayer
from Connect4Game import Connect4Game

def main():
    # 1. Configurar a Simulação
    num_jogos = 100

    # O teu bot (Peça 1) vs Bot Aleatório (Peça 2)
    # Podes manter as 500 iterações por agora, ou subir para 1000 se o teu PC for rápido
    p1 = MCTSAIPlayer(piece=1, max_iterations=500)
    p2 = RandomAIPlayer(piece=2)

    game = Connect4Game()

    # 2. Variáveis para guardar as estatísticas
    vitorias_p1 = 0
    vitorias_p2 = 0
    empates = 0
    tempos_de_jogo = []

    print(f"A iniciar {num_jogos} jogos automáticos (MCTS vs Aleatório)...")

    # 3. O Ciclo de Torneio
    for i in range(num_jogos):
        tempo_inicio = time.time() # Começa a contar o tempo

        # headless=True faz o jogo correr de forma invisível e super rápida
        vencedor = game.run_game(p1, p2, headless=True)

        tempo_fim = time.time() # Pára o cronómetro

        # Guarda a duração deste jogo na lista
        tempos_de_jogo.append(tempo_fim - tempo_inicio)

        # Regista quem ganhou
        if vencedor == 1:
            vitorias_p1 += 1
        elif vencedor == 2:
            vitorias_p2 += 1
        else:
            empates += 1

        # Para saberes que o programa não bloqueou, imprime um aviso a cada 10 jogos
        if (i + 1) % 10 == 0:
            print(f"[{i + 1}/{num_jogos}] jogos concluídos...")

    # 4. Calcular as Estatísticas Finais para o Excel
    taxa_vitorias_p1 = (vitorias_p1 / num_jogos) * 100
    taxa_vitorias_p2 = (vitorias_p2 / num_jogos) * 100

    tempo_medio = sum(tempos_de_jogo) / len(tempos_de_jogo)
    tempo_maximo = max(tempos_de_jogo)
    tempo_minimo = min(tempos_de_jogo)

    # 5. Imprimir o "Talão" de Resultados
    print("\n" + "="*40)
    print("🎯 RESULTADOS FINAIS PARA O EXCEL 🎯")
    print("="*40)
    print(f"Confronto: MCTS (1) vs Aleatório (2)")
    print(f"Nº de Jogos: {num_jogos}")
    print(f"Vitórias Jogador 1 (MCTS): {vitorias_p1}")
    print(f"Vitórias Jogador 2 (Aleatório): {vitorias_p2}")
    print(f"Empates: {empates}")
    print(f"Taxa de Vitórias Jogador 1: {taxa_vitorias_p1:.2f}%")
    print(f"Taxa de Vitórias Jogador 2: {taxa_vitorias_p2:.2f}%")
    print("-" * 40)
    print(f"Duração Média do Jogo: {tempo_medio:.4f} segundos")
    print(f"Duração Máxima: {tempo_maximo:.4f} segundos")
    print(f"Duração Mínima: {tempo_minimo:.4f} segundos")
    print("="*40)

if __name__ == "__main__":
    main()