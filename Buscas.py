from collections import deque
import heapq

# Criar grafo com pesos
grafo = {}

heuristica = {
    'araraquara': 98,
    'jaboticabal': 153,
    'taquaritinga': 148,
    'ribeirao_preto': 149,
    'porto_ferreira': 85,
    'sao_carlos': 71,
    'jau': 91,
    'brotas': 60,
    'pirassununga': 71,
    'rio_claro': 32,
    'limeira': 25,
    'piracicaba': 0  # objetivo
}

arestas = [
    ('jaboticabal', 'ribeirao_preto', 50),
    ('jaboticabal', 'araraquara', 62),
    ('jaboticabal', 'taquaritinga', 25),
    ('taquaritinga', 'araraquara', 56),
    ('araraquara', 'ribeirao_preto', 79),
    ('araraquara', 'jau', 66),
    ('araraquara', 'sao_carlos', 38),
    ('sao_carlos', 'jau', 85),
    ('sao_carlos', 'brotas', 59),
    ('jau', 'brotas', 47),
    ('brotas', 'piracicaba', 71),
    ('ribeirao_preto', 'sao_carlos', 87),
    ('ribeirao_preto', 'porto_ferreira', 77),
    ('porto_ferreira', 'sao_carlos', 47),
    ('porto_ferreira', 'pirassununga', 17),
    ('pirassununga', 'sao_carlos', 52),
    ('pirassununga', 'rio_claro', 57),
    ('pirassununga', 'limeira', 65),
    ('rio_claro', 'sao_carlos', 53),
    ('rio_claro', 'limeira', 28),
    ('rio_claro', 'piracicaba', 35),
    ('limeira', 'piracicaba', 32),
]

# DFS com custo acumulado
def busca_dfs(grafo, atual, destino, caminho=None, visitados=None, custo=0):
    if caminho is None:
        caminho = [atual]
    if visitados is None:
        visitados = set()
    visitados.add(atual)

    if atual == destino:
        return caminho, custo

    for vizinho, tempo in grafo.get(atual, []):
        if vizinho not in visitados:
            resultado = busca_dfs(grafo, vizinho, destino, caminho + [vizinho], visitados, custo + tempo)
            if resultado:
                return resultado

    return None


# BFS com custo acumulado
def busca_bfs(grafo, inicio, destino):
    fila = deque()
    fila.append(([inicio], 0))  # (caminho, custo total)
    visitados = set()

    while fila:
        caminho, custo = fila.popleft()
        atual = caminho[-1]

        if atual == destino:
            return caminho, custo

        if atual not in visitados:
            visitados.add(atual)
            for vizinho, tempo in grafo.get(atual, []):
                if vizinho not in caminho:  # Evita ciclos
                    nova_rota = list(caminho)
                    nova_rota.append(vizinho)
                    fila.append((nova_rota, custo + tempo))
    return None


def busca_a_estrela(grafo, heuristica, inicio, destino):
    fila = []
    heapq.heappush(fila, (heuristica.get(inicio, float('inf')), 0, [inicio]))  # (f = g + h, g, caminho)

    visitados = set()

    while fila:
        f_total, custo_atual, caminho = heapq.heappop(fila)
        atual = caminho[-1]

        if atual == destino:
            return caminho, custo_atual

        if atual not in visitados:
            visitados.add(atual)
            for vizinho, custo in grafo.get(atual, []):
                if vizinho not in visitados:
                    novo_caminho = caminho + [vizinho]
                    novo_custo = custo_atual + custo
                    f = novo_custo + heuristica.get(vizinho, float('inf'))
                    heapq.heappush(fila, (f, novo_custo, novo_caminho))

    return None

# Menu

vias_bloqueadas = []
print("Deseja bloquear alguma via? (Ex: araraquara-sao_carlos). Digite 'ok' para continuar.")
while True:
    bloqueio = input("Via bloqueada: ").strip().lower()
    if bloqueio == "ok":
        break
    try:
        origem, destino = bloqueio.split("-")
        vias_bloqueadas.append((origem, destino))
    except ValueError:
        print("Formato inválido. Use o formato cidade1-cidade2.")

# Construir grafo com pesos (não-direcionado)
for origem, destino, tempo in arestas:
    if (origem, destino) in vias_bloqueadas or (destino, origem) in vias_bloqueadas:
        continue  # Pula vias bloqueadas
    grafo.setdefault(origem, []).append((destino, tempo))
    grafo.setdefault(destino, []).append((origem, tempo))

while True:
    print("\n====== MENU ======")
    print("0 - Sair")
    print("1 - Busca em profundidade (DFS)")
    print("2 - Busca em largura (BFS)")
    print("3 - Busca A* (melhor caminho com heurística)")


    try:
        escolha = int(input("Escolha uma opção: "))
    except ValueError:
        print("Por favor, digite um número válido.")
        continue

    if escolha == 0:
        break

    elif escolha in (1, 2, 3):
        inicio = input("Digite a cidade inicial: ").strip().lower()
        fim = input("Digite a cidade final: ").strip().lower()

        if inicio not in grafo or fim not in grafo:
            print("Cidade inválida! Verifique o nome digitado.")
            continue

        if escolha == 1:
            resultado_dfs = busca_dfs(grafo, inicio, fim)
            print("\nBusca em Profundidade (DFS):")
            if resultado_dfs:
                caminho, custo = resultado_dfs
                print(" -> ".join(caminho))
                print(f"Tempo total: {custo} minutos")
            else:
                print("Caminho não encontrado.")

        elif escolha == 2:
            resultado_bfs = busca_bfs(grafo, inicio, fim)
            print("\nBusca em Largura (BFS):")
            if resultado_bfs:
                caminho, custo = resultado_bfs
                print(" -> ".join(caminho))
                print(f"Tempo total: {custo} minutos")
            else:
                print("Caminho não encontrado.")

        elif escolha == 3:
            resultado_astar = busca_a_estrela(grafo, heuristica, inicio, fim)
            print("\nBusca A* (A estrela):")
            if resultado_astar:
                caminho, custo = resultado_astar
                print(" -> ".join(caminho))
                print(f"Tempo total: {custo} minutos")
        else:
            print("Caminho não encontrado.")

    else:
        print("Opção inválida. Tente novamente.")