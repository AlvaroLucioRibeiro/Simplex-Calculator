import numpy as np

# Função para realizar operações de pivoteamento na tabela simplex.
def pivot_on(tableau, row, col):
    nr, nc = tableau.shape  # Obtém o número de linhas (nr) e colunas (nc) do tableau.
    pivot = tableau[row, col]  # Elemento de pivô.
    tableau[row, :] /= pivot  # Transforma o elemento de pivô em 1 dividindo toda a linha por ele.
    for r in range(nr):  # Para cada linha no tableau...
        if r == row:  # Exceto a linha do pivô...
            continue
        # Subtrai um múltiplo da linha do pivô para zerar o elemento na coluna do pivô.
        tableau[r, :] -= tableau[r, col] * tableau[row, :]

# Função principal do método simplex.
def simplex(c, A, b, maximize=True):
    if not maximize:  # Se o problema é de minimização...
        c = -c  # Inverte os sinais dos coeficientes da função objetivo.
        
    # Construção do tableau inicial.
    A = np.hstack((A, np.eye(len(A))))  # Adiciona as variáveis de folga à matriz de restrições A.
    c = np.concatenate((c, np.zeros(len(A))))  # Adiciona zeros correspondentes às variáveis de folga na função objetivo.
    tableau = np.vstack((A, c))  # Combina A e c para formar o tableau.
    b = np.concatenate((b, [0]))  # Adiciona o lado direito das restrições e o valor da função objetivo (0) ao tableau.
    tableau = np.column_stack((tableau, b))  # Adiciona a coluna do lado direito ao tableau.

    # Processo iterativo do método simplex.
    while (maximize and np.any(tableau[-1, :-1] < 0)) or (not maximize and np.any(tableau[-1, :-1] > 0)):
        # Escolha da coluna do pivô (coluna de entrada).
        if maximize:
            col = np.argmin(tableau[-1, :-1])  # Para maximização: escolhe o menor valor negativo na linha da função objetivo.
        else:
            col = np.argmax(tableau[-1, :-1])  # Para minimização: escolhe o maior valor na linha da função objetivo.
        # Se todos os elementos na coluna do pivô são ≤ 0, então o problema é ilimitado (sem solução ótima).
        if np.all(tableau[:, col] <= 0):
            raise ValueError("Problema sem solução.")
        # Escolha da linha do pivô (linha de saída).
        ratios = tableau[:-1, -1] / tableau[:-1, col]  # Calcular as razões entre o lado direito e os elementos da coluna do pivô.
        row = np.argmin(np.where(tableau[:-1, col] > 0, ratios, np.inf))  # A linha do pivô é a que tem o menor valor positivo na razão.
        pivot_on(tableau, row, col)  # Realiza a operação de pivoteamento.

    # Após concluir as iterações, os preços sombra podem ser encontrados na última linha do tableau (negativos para maximização).
    shadow_prices = -tableau[-1, len(c)-len(A):len(c)]  # Apenas os preços sombra das restrições originais.
    
    return tableau, shadow_prices

# Exemplo de entrada com os coeficientes corretos para maximização
c = np.array([-3, -1, -5])  # Coeficientes da função objetivo com sinais corretos para maximização
A = np.array([[6, 3, -5], [3, 4, 5]])  # Coeficientes das restrições
b = np.array([45, 30])  # LDs das restrições

# Execução do algoritmo simplex
tableau, shadow_prices = simplex(c, A, b, maximize=True)
# Obtém a solução ótima e o valor ótimo a partir do tableau final
optimal_solution = tableau[:-1, -1]
optimal_value = tableau[-1, -1]
# Ajusta os preços sombra para terem o sinal correto
shadow_prices[shadow_prices != 0] = -shadow_prices[shadow_prices != 0]

# Formatação da saída da solução ótima
optimal_solution = optimal_solution[:]
print("Solução Ótima:", optimal_solution)
print("Valor Ótimo:", optimal_value)
print("Preços Sombra:", shadow_prices)
