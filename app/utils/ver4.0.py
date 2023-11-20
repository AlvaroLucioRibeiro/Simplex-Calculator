import numpy as np
from itertools import combinations

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
def simplex(c, A, b, comparisons):
    if len(comparisons) != len(A):
        raise ValueError("Número de comparações deve ser igual ao número de restrições.")

    # Ajustando o tableau para diferentes comparações
    aux_A = np.eye(len(A))
    for i, comp in enumerate(comparisons):
        if comp == 'greater':
            for j in range(len(aux_A[i])):
                if aux_A[i][j] != 0:
                    aux_A[i][j] = -aux_A[i][j]  # Inverte a restrição para '<='
        elif comp != 'less':
            raise ValueError("Comparação inválida. Use 'less' ou 'greater'.")

    # Restante do código para construir o tableau
    A = np.hstack((A, aux_A))  # Adiciona as variáveis de folga
    c = np.concatenate((c, np.zeros(len(A))))  # Zeros para as variáveis de folga
    tableau = np.vstack((A, c))  # Combina A e c
    b = np.concatenate((b, [0]))  # Lado direito das restrições e valor da função objetivo
    tableau = np.column_stack((tableau, b))  # Adiciona a coluna do lado direito

    print(f"A:\n{A}\n---")

    # Processo iterativo do método simplex
    while np.any(tableau[-1, :-1] < 0):
        col = np.argmin(tableau[-1, :-1])  # Coluna de entrada
        if np.all(tableau[:, col] <= 0):
            raise ValueError("Problema sem solução.")

        ratios = tableau[:-1, -1] / tableau[:-1, col]  # Razões
        row = np.argmin(np.where(tableau[:-1, col] > 0, ratios, np.inf))
        pivot_on(tableau, row, col)

    # Após concluir as iterações, os preços sombra podem ser encontrados na última linha do tableau (negativos para maximização).
    shadow_prices = -tableau[-1, len(c)-len(A):len(c)]  # Apenas os preços sombra das restrições originais.

    return tableau, shadow_prices

# Exemplo de entrada com os coeficientes corretos para maximização
c = np.array([-6, -4, -6, -8])  # Coeficientes da função objetivo com sinais corretos para maximização
A = np.array([[3, 2, 2, 4], [1, 1, 2, 3], [2, 1, 2, 1], [1, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 1]])  # Coeficientes das restrições
b = np.array([480, 400, 400, 50, 100, 25])  # LDs das restrições

comparisons = ['less', 'less','less', 'greater', 'greater', 'less']  # Define a comparação para cada restrição

# Execução do algoritmo simplex
tableau, shadow_prices = simplex(c, A, b, comparisons)

print(f"Tabelau\n{tableau}\n")

# Obtém a solução ótima e o valor ótimo a partir do tableau final
optimal_solution = tableau[:-1, -1]
optimal_value = tableau[-1, -1]

# Ajusta os preços sombra para terem o sinal correto
shadow_prices[shadow_prices != 0] = -shadow_prices[shadow_prices != 0]

# Função para ajustar -0 para 0
def adjust_shadow_prices(shadow_prices):
    return np.where(shadow_prices == -0.0, 0.0, shadow_prices)

# Ajusta os preços sombra antes de imprimi-los
adjusted_shadow_prices = adjust_shadow_prices(shadow_prices)

# --------------------------------------- Saída de Dados --------------------------------------- #

# Formatação da saída da solução ótima
optimal_solution = optimal_solution[:]
print("Solução Ótima:", optimal_solution)
print("Valor Ótimo:", optimal_value)
print("Preços Sombra:", adjusted_shadow_prices)

# Função ajustada para extrair as variáveis de decisão originais da solução ótima
def extract_decision_variables_corrected(optimal_solution, num_decision_vars):
    return optimal_solution[-num_decision_vars:]

# Ajustando a extração das variáveis de decisão originais
decision_vars_corrected = extract_decision_variables_corrected(optimal_solution, len(c) - 1)
print(f"Variáveis de decisão corretas: {decision_vars_corrected}")