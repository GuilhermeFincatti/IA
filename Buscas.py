from collections import deque
from Dados import heuristica_AQA, heuristica_JAU, arestas, cidades
import heapq
import os

# Função para limpar o terminal
def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Criar grafo
grafo = {}

# Busca em profundidade
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


# Busca em largura
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


# Busca heuristica A*
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

# Main
vias_bloqueadas = []
print("Deseja bloquear alguma via? (Ex: araraquara-sao_carlos). Digite 'ok' para continuar.")

# Inserção das vias bloqueadas
while True:
    bloqueio = input("\nVia bloqueada: ").strip().lower()
    if bloqueio == "ok":
        break

    # Tratamento de erro caso o formato das cidades não tenham sido inseridas corretamente
    try:                                            
        origem, destino = bloqueio.split("-")
        # Tratamento de erro caso o nome de alguma cidade seja inválido ou caso a rota não exista
        if (origem or destino) not in cidades:
            print("Via inválida. Verifique a via digitada.")
            continue
        else:
            vias_bloqueadas.append((origem, destino))   # Adiciona par a lista de vias_bloqueadas
    except ValueError:
        print("Formato inválido. Use o formato cidade1-cidade2.")


# Construindo grafo com custos
for origem, destino, tempo in arestas:
    # Condição para não inserir as vias bloqueadas
    if (origem, destino) in vias_bloqueadas or (destino, origem) in vias_bloqueadas:    
        continue
    grafo.setdefault(origem, []).append((destino, tempo))
    grafo.setdefault(destino, []).append((origem, tempo))

# Limpando terminal
limpar_terminal()

# Menu
while True:
    print("\t MENU")
    print("0 - Sair")
    print("1 - Busca em profundidade")
    print("2 - Busca em largura")
    print("3 - Busca A*")

    # Tratamento de erro para entradas diferentes de números inteiros
    try:
        escolha = int(input("Escolha uma opção: "))
    except ValueError:
        print("Por favor, digite um número válido.")
        continue

    # Saindo do Menu
    if escolha == 0:
        break

    elif escolha in (1, 2, 3):
        # Inserção das cidades de origem e destino
        inicio = input("Digite a cidade inicial: ").strip().lower()
        fim = input("Digite a cidade final: ").strip().lower()

        # Tratamento de erro para caso a cidade inserida não esteja mapeada no grafo, ou foi digitada incorretamente
        if inicio not in grafo or fim not in grafo:
            print("Cidade inválida! Verifique o nome digitado.")
            continue

        # Caso Busca em Profundidade
        if escolha == 1:
            resultado_dfs = busca_dfs(grafo, inicio, fim)
            print("\nBusca em Profundidade (DFS):")
            if resultado_dfs:
                caminho, custo = resultado_dfs
                print(" -> ".join(caminho))
                print(f"Tempo total: {custo} minutos")
            else:
                print("Caminho não encontrado.")

        # Caso Busca em Largura
        elif escolha == 2:
            resultado_bfs = busca_bfs(grafo, inicio, fim)
            print("\nBusca em Largura (BFS):")
            if resultado_bfs:
                caminho, custo = resultado_bfs
                print(" -> ".join(caminho))
                print(f"Tempo total: {custo} minutos")
            else:
                print("Caminho não encontrado.")

        # Caso Busca Heurística A*
        elif escolha == 3:
            # Tratamento do erro, para qualquer caso em que não foram mapeados os custos estimados do par(origem-destino), fundamental para o funcionamento da busca A*
            if inicio == "araraquara" and fim == "piracicaba":                         
                resultado_astar = busca_a_estrela(grafo, heuristica_AQA, inicio, fim)   
            elif inicio == "jau" and fim == "ribeirao_preto":                           
                resultado_astar = busca_a_estrela(grafo, heuristica_JAU, inicio, fim)   
            else:
                print("Custos Estimados não mapeados.")                                 
                continue
    
            print("\nBusca A*:")
            if resultado_astar:
                caminho, custo = resultado_astar
                print(" -> ".join(caminho))
                print(f"Tempo total: {custo} minutos")
        else:
            print("Caminho não encontrado.")

    # Em caso de um numero diferente das opções dadas pelo MENU
    else:
        print("Opção inválida. Tente novamente.")