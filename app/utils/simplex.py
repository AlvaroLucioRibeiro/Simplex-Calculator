from typing import Dict, List
import numpy as np

class Simplex():
    # Simplex Setup
    def __init__(self, tipo_problema, n_var, n_restricoes, coefs_funcao_objetivo, coefs_restricoes, lados_direitos, sinais) -> None:
        self.n_var = n_var # Número de variáveis
        self.n_restricoes = n_restricoes # Número de restrições
        self.c = coefs_funcao_objetivo # Lista de cada coeficiente da função objetivo. Ex.: Z = 5A + 3B coefs_funcao_objetivo = [5, 3]
        self.A = coefs_restricoes # Lista de cada coeficiente das restrições. Ex.: 10A + 3B < 30; 13A + 12B >= 55; 32A + 9B >= 78 coefs_restricoes = [[10, 3], [13, 12], [32, 9]]
        self.b = lados_direitos  # Lista de cada coeficiente de restrição do Lado Direito da equação. Ex.: 10A + 3B < 30; 13A + 12B >= 55; 32A + 9B >= 78 lados_direitos = [30, 55, 78]
        self.sinais = sinais # Indica se o sinal é maior igual ou menor de cada equação das restrições. Ex.: Ex.: 10A + 3B < 30; 13A + 12B >= 55; 32A + 9B >= 78 sinais = ['less', 'greater', 'greater']

        self.maximize = True if tipo_problema == 'max' else False # Definir tipo do problema

    # Função para realizar operações de pivoteamento na tabela simplex.
    def pivot_on(self):
        nr, nc = self.tableau.shape  # Obtém o número de linhas (nr) e colunas (nc) do tableau.
        pivot = self.tableau[self.row, self.col]  # Elemento de pivô.
        self.tableau[self.row, :] /= pivot  # Transforma o elemento de pivô em 1 dividindo toda a linha por ele.
        for r in range(nr):  # Para cada linha no tableau...
            if r == self.row:  # Exceto a linha do pivô...
                continue
            # Subtrai um múltiplo da linha do pivô para zerar o elemento na coluna do pivô.
            self.tableau[r, :] -= self.tableau[r, self.col] * self.tableau[self.row, :]

    # Função principal do método simplex.
    def simplex(self):
        if not self.maximize:  # Se o problema é de minimização...
            self.c = -self.c  # Inverte os sinais dos coeficientes da função objetivo.
        
        # Construção do tableau inicial.
        print(f'A: {self.A} e c: {self.c}')
        self.A = np.hstack((self.A, np.eye(len(self.A))))  # Adiciona as variáveis de folga à matriz de restrições A.
        self.c = np.concatenate((self.c, np.zeros(len(self.A))))  # Adiciona zeros correspondentes às variáveis de folga na função objetivo.
        self.tableau = np.vstack((self.A, self.c))  # Combina A e c para formar o tableau.
        self.b = np.concatenate((self.b, [0]))  # Adiciona o lado direito das restrições e o valor da função objetivo (0) ao tableau.
        self.tableau = np.column_stack((self.tableau, self.b))  # Adiciona a coluna do lado direito ao tableau.

        # Processo iterativo do método simplex.
        while (self.maximize and np.any(self.tableau[-1, :-1] < 0)) or (not self.maximize and np.any(self.tableau[-1, :-1] > 0)):
            # Escolha da coluna do pivô (coluna de entrada).
            if self.maximize:
                self.col = np.argmin(self.tableau[-1, :-1])  # Para maximização: escolhe o menor valor negativo na linha da função objetivo.
            else:
                self.col = np.argmax(self.tableau[-1, :-1])  # Para minimização: escolhe o maior valor na linha da função objetivo.
            # Se todos os elementos na coluna do pivô são ≤ 0, então o problema é ilimitado (sem solução ótima).
            if np.all(self.tableau[:, self.col] <= 0):
                raise ValueError("Problema sem solução.")
            # Escolha da linha do pivô (linha de saída).
            ratios = self.tableau[:-1, -1] / self.tableau[:-1, self.col]  # Calcular as razões entre o lado direito e os elementos da coluna do pivô.
            self.row = np.argmin(np.where(self.tableau[:-1, self.col] > 0, ratios, np.inf))  # A linha do pivô é a que tem o menor valor positivo na razão.
            self.pivot_on()  # Realiza a operação de pivoteamento.

        # Após concluir as iterações, os preços sombra podem ser encontrados na última linha do tableau (negativos para maximização).
        shadow_prices = -self.tableau[-1, len(self.c)-len(self.A):len(self.c)]  # Apenas os preços sombra das restrições originais.

        # Obtém a solução ótima e o valor ótimo a partir do tableau final
        optimal_solution = self.tableau[:-1, -1]
        optimal_value = self.tableau[-1, -1]
        # Ajusta os preços sombra para terem o sinal correto
        shadow_prices[shadow_prices != 0] = -shadow_prices[shadow_prices != 0]

        print(f'Tableau: {self.tableau}')
        
        return optimal_solution, optimal_value, shadow_prices
