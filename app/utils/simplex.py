from typing import Dict, List
import numpy as np

class Simplex():
    # Simplex Setup
    def __init__(self, n_var, n_restricoes, coefs_funcao_objetivo, coefs_restricoes, lados_direitos, sinais) -> None:
        self.n_var = n_var # Número de variáveis
        self.n_restricoes = n_restricoes # Número de restrições
        self.c = coefs_funcao_objetivo # Lista de cada coeficiente da função objetivo. Ex.: Z = 5A + 3B coefs_funcao_objetivo = [5, 3]
        self.A = coefs_restricoes # Lista de cada coeficiente das restrições. Ex.: 10A + 3B < 30; 13A + 12B >= 55; 32A + 9B >= 78 coefs_restricoes = [[10, 3], [13, 12], [32, 9]]
        self.b = lados_direitos  # Lista de cada coeficiente de restrição do Lado Direito da equação. Ex.: 10A + 3B < 30; 13A + 12B >= 55; 32A + 9B >= 78 lados_direitos = [30, 55, 78]
        self.sinais = sinais # Indica se o sinal é maior igual ou menor de cada equação das restrições. Ex.: Ex.: 10A + 3B < 30; 13A + 12B >= 55; 32A + 9B >= 78 sinais = ['less', 'greater', 'greater']

    # Função para realizar operações de pivoteamento na tabela simplex.
    def pivot_on(self):
        nr, nc = self.tableau.shape  # Obtém o número de linhas (nr) e self.colunas (nc) do self.tableau.
        pivot = self.tableau[self.row, self.col]  # Elemento de pivô.
        self.tableau[self.row, :] /= pivot  # Transforma o elemento de pivô em 1 dividindo toda a linha por ele.
        for r in range(nr):  # Para cada linha no self.tableau...
            if r == self.row:  # Exceto a linha do pivô...
                continue
            # Subtrai um múltiplo da linha do pivô para zerar o elemento na self.coluna do pivô.
            self.tableau[r, :] -= self.tableau[r, self.col] * self.tableau[self.row, :]

    # Função principal do método simplex.
    def simplex(self):
        if len(self.sinais) != len(self.A):
            raise ValueError("Número de comparações deve ser igual ao número de restrições.")

        # Ajustando o tableau para diferentes comparações
        aux_A = np.eye(len(A))
        for i, comp in enumerate(self.sinais):
            if comp == 'greater':
                for j in range(len(aux_A[i])):
                    if aux_A[i][j] != 0:
                        aux_A[i][j] = -aux_A[i][j]  # Inverte a restrição para '<='
            elif comp != 'less':
                raise ValueError("Comparação inválida. Use 'less' ou 'greater'.")

        # Restante do código para construir o tableau
        self.A = np.hstack((self.A, aux_A))  # Adiciona as variáveis de folga
        self.c = np.concatenate((self.c, np.zeros(len(self.A))))  # Zeros para as variáveis de folga
        self.tableau = np.vstack((self.A, self.c))  # Combina A e c
        self.b = np.concatenate((self.b, [0]))  # Lado direito das restrições e valor da função objetivo
        self.tableau = np.column_stack((self.tableau, self.b))  # Adiciona a coluna do lado direito
        print(f"Tableau Inicial: {self.tableau}")

        # Processo iterativo do método simplex
        while np.any(self.tableau[-1, :-1] < 0):
            self.col = np.argmin(self.tableau[-1, :-1])  # Coluna de entrada
            if np.all(self.tableau[:, self.col] <= 0):
                raise ValueError("Problema sem solução.")

            ratios = self.tableau[:-1, -1] / self.tableau[:-1, self.col]  # Razões
            self.row = np.argmin(np.where(self.tableau[:-1, self.col] > 0, ratios, np.inf))
            self.pivot_on()

        # Após concluir as iterações, os preços sombra podem ser encontrados na última linha do tableau (negativos para maximização).
        self.shadow_prices = -self.tableau[-1, len(self.c)-len(self.A):len(self.c)]  # Apenas os preços sombra das restrições originais.
        # Ajusta os preços sombra para terem o sinal correto
        self.shadow_prices[self.shadow_prices != 0] = -self.shadow_prices[self.shadow_prices != 0]
        # Função para ajustar -0 para 0
        self.shadow_prices = np.where(self.shadow_prices == -0.0, 0.0, self.shadow_prices)
        
        # Obtém a solução ótima e o valor ótimo a partir do tableau final
        #optimal_solution = self.tableau[:-1, -1]
        self.optimal_solution = []
        for list in self.tableau:
            self.optimal_solution.append(list[-1])

        self.optimal_solution.pop() # Remove último elemento

        while(len(self.optimal_solution) > self.n_var):
            self.optimal_solution.pop(0)

        print(f"Optimal solution initial: {self.optimal_solution}")
        self.optimal_value = self.tableau[-1, -1]
        if(len(self.optimal_solution) < self.n_var):
            self.optimal_solution.append(0.0)

        print(f"Tableau Final: {self.tableau}")

        return self.optimal_solution, self.optimal_value, self.shadow_prices


# Exemplo de entrada com os coeficientes corretos para maximização
c = np.array([-3000, -5000])  # Coeficientes da função objetivo com sinais corretos para maximização
A = np.array([[0.5, 0.2], [0.25, 0.3], [0.25, 0.5]])  # Coeficientes das restrições
b = np.array([16,11,15])  # LDs das restrições
comparisons = ['less', 'less', 'less']  # Define a comparação para cada restrição
# RESULTADO CORRETO: $160.000 -> (20,20)


'''
# Exemplo de entrada com os coeficientes corretos para maximização
c = np.array([-5, -7, -8])  # Coeficientes da função objetivo com sinais corretos para maximização
A = np.array([[1, 1, 2], [3, 4.5, 1]])  # Coeficientes das restrições
b = np.array([1190, 4000])  # LDs das restrições
comparisons = ['less', 'less']  # Define a comparação para cada restrição
# RESULTADO CORRETO: $7313.75 -> (0; 851.25; 169.38)
'''

'''
# Exemplo de entrada com os coeficientes corretos para maximização
c = np.array([-6, -4, -6, -8])  # Coeficientes da função objetivo com sinais corretos para maximização
A = np.array([[3, 2, 2, 4], [1, 1, 2, 3], [2, 1, 2, 1], [1, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 1]])  # Coeficientes das restrições
b = np.array([480, 400, 400, 50, 100, 25])  # LDs das restrições
comparisons = ['less', 'less','less', 'greater', 'greater', 'less']  # Define a comparação para cada restrição
# RESULTADO CORRETO: $1250 -> (50, 0, 145, 10)
'''

teste = Simplex(2, 3, c, A, b, comparisons)
# Execução do algoritmo simplex
optimal_solution, optimal_value, shadow_prices = teste.simplex()

# --------------------------------------- Saída de Dados --------------------------------------- #

# Formatação da saída da solução ótima
#optimal_solution = optimal_solution[:]
print("Solução Ótima:", optimal_solution)
print("Valor Ótimo:", optimal_value)
print("Preços Sombra:", shadow_prices)

# Função ajustada para extrair as variáveis de decisão originais da solução ótima
def extract_decision_variables_corrected(optimal_solution, num_decision_vars):
    return optimal_solution[-num_decision_vars:]

# Ajustando a extração das variáveis de decisão originais
decision_vars_corrected = extract_decision_variables_corrected(optimal_solution, len(c) - 1)
print(f"Variáveis de decisão corretas: {decision_vars_corrected}")
