from collections import deque
from Dados import heuristica_AQA, heuristica_JAU, arestas, cidades
import heapq
import os
import random

# Função para limpar o terminal
def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Criar grafo
grafo = {}

# Busca em profundidade
def busca_profundidade(grafo, atual, destino, caminho=None, visitados=None, custo=0):

    # Primeiro chamada caminho = atual = inicio
    if caminho is None:
        caminho = [atual]
    # Primeiro chamada cria conjunto para armazenar valores de visitados (set() elimina duplicatas)
    if visitados is None:
        visitados = set()

    visitados.add(atual)

    # Condição de parada
    if atual == destino:
        return caminho, custo

    # Para todos os vizinhos do nó atual
    for vizinho, tempo in grafo.get(atual, []):
        # Recursão caso o vizinho nao tenha sido visitado, enviando novo caminho, novos visitados e somando o tempo ao custo (buscando profundamente)
        if vizinho not in visitados:
            resultado = busca_profundidade(grafo, vizinho, destino, caminho + [vizinho], visitados, custo + tempo)
            if resultado:
                return resultado
    return None

# Busca em largura
def busca_largura(grafo, inicio, destino):

    # Fila com possibilidade de inserção e remoção tanto no início quanto no fim
    fila = deque()
    # (Caminho, Custo total)
    fila.append(([inicio], 0))  
    visitados = set()

    while fila:
        # Armazena (Caminho e Custo total) nas variáveis caminho e custo, retirando o primeiro elemento da fila
        caminho, custo = fila.popleft()
        # # Armazena a ultima cidade da fila no nó atual, pois foi a última cidade visitada
        atual = caminho[-1]

        # Condição de parada
        if atual == destino:
            return caminho, custo

        if atual not in visitados:
            visitados.add(atual)
            # Pera todos os vizinhos do nó atual
            for vizinho, tempo in grafo.get(atual, []):
                # Evita ciclos
                if vizinho not in caminho:  
                    # Adiciona vizinhos que ainda nao tenham sidos visitados na fila para serem explorados depois
                    nova_rota = list(caminho)
                    nova_rota.append(vizinho)
                    fila.append((nova_rota, custo + tempo))
    return None


# Busca heuristica A*
def busca_a_estrela(grafo, heuristica, inicio, destino):
    fila = []
    # Cria uma min-heap que armazena os elementos da fila ordenados pelo menor valor de f, prioridade determinada pelo primeiro elemento da tupla
    heapq.heappush(fila, (heuristica.get(inicio, float('inf')), 0, [inicio]))
    visitados = set()

    while fila:
        # Armazena o nó com menor f nas variáveis, heappop() sempre tirará o primeiro elemento da fila, que neste caso é o menor
        f_total, custo_atual, caminho = heapq.heappop(fila)
        # Armazena a ultima cidade da fila no nó atual
        atual = caminho[-1]

        # Condição de parada
        if atual == destino:
            return caminho, custo_atual


        if atual not in visitados:
            visitados.add(atual)
            # Para todos os vizinhos do nó atual
            for vizinho, custo in grafo.get(atual, []):
                if vizinho not in visitados:
                    # Calcula novo caminho, custo e sua heurística e em seguida 
                    novo_caminho = caminho + [vizinho]
                    novo_custo = custo_atual + custo
                    # f(n) = g(n) + h(n)
                    f = novo_custo + heuristica.get(vizinho, float('inf')) 
                    # Insere na min-heap este novo caminho
                    heapq.heappush(fila, (f, novo_custo, novo_caminho))
    return None

# Main
vias_bloqueadas = []
vias_obstruidas = []

# Inserção das vias bloqueadas
print("Deseja BLOQUEAR alguma via direta? (Ex: araraquara-sao_carlos). Digite 'ok' para continuar.")

while True:
    bloqueio = input("\nVia bloqueada: ").strip().lower()
    if bloqueio == "ok":
        break

    # Tratamento de erro caso o formato das cidades não tenham sido inseridas corretamente
    try:                                            
        origem, destino = bloqueio.split("-")
        # Tratamento de erro caso o nome de alguma cidade seja inválido ou caso a rota não exista
        if origem not in cidades or destino not in cidades: 
            print("Via inválida. Verifique a via digitada.")
            continue
        else:
            vias_bloqueadas.append((origem, destino))   # Adiciona par a lista de vias_bloqueadas
    except ValueError:
        print("Formato inválido. Use o formato cidade1-cidade2.")

# Limpando terminal
limpar_terminal()

# Inserção de vias obstruidas
print("Deseja OBSTRUIR alguma via direta? (Ex: araraquara-sao_carlos). Digite 'ok' para continuar.")

while True:
    obstruida = input("\nVia obstruida: ").strip().lower()
    if obstruida == "ok":
        break

    # Tratamento de erro caso o formato das cidades não tenham sido inseridas corretamente
    try:                                            
        origem, destino = obstruida.split("-")
        # Tratamento de erro caso o nome de alguma cidade seja inválido ou caso a rota não exista
        if origem not in cidades or destino not in cidades:
            print("Via inválida. Verifique a via digitada.")
            continue
        else:
            vias_obstruidas.append((origem, destino))   # Adiciona par a lista de vias_bloqueadas
    except ValueError:
        print("Formato inválido. Use o formato cidade1-cidade2.")

# Construindo grafo com custos
for origem, destino, tempo in arestas:
    # Condição para não inserir as vias bloqueadas
    if (origem, destino) in vias_bloqueadas or (destino, origem) in vias_bloqueadas:    
        continue
    # Condição para inserir transito nas vias, geração do transito randomicamente
    if (origem, destino) in vias_obstruidas or (destino, origem) in vias_obstruidas:
        transito = random.randint(10,30)
        tempo = tempo + transito
        # Impressao na terminal para interface ficar intuitiva
        print(f"\nDevido às vias obstruídas as vias de: {origem}-{destino} estão com novo tempo de: {tempo} minutos")
    grafo.setdefault(origem, []).append((destino, tempo))
    grafo.setdefault(destino, []).append((origem, tempo))

# Menu
while True:
    print("\n\t MENU")
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
            resultado_profundidade = busca_profundidade(grafo, inicio, fim)
            print("\nBusca em Profundidade:")
            if resultado_profundidade:
                caminho, custo = resultado_profundidade
                print(" -> ".join(caminho))
                print(f"Tempo total: {custo} minutos")
            else:
                print("Caminho não encontrado.")

        # Caso Busca em Largura
        elif escolha == 2:
            resultado_largura = busca_largura(grafo, inicio, fim)
            print("\nBusca em Largura:")
            if resultado_largura:
                caminho, custo = resultado_largura
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