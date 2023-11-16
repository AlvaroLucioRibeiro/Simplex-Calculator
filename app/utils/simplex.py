from typing import Dict, List
import numpy as np

class Simplex():
    # Simplex Setup
    def __init__(self, tipo_problema, n_var, n_restricoes, coefs_funcao_objetivo, coefs_restricoes, lados_direitos, sinais) -> None:
        self.tipo_problema: str = tipo_problema # "max" or "min"
        self.n_var = n_var # Número de variáveis
        self.n_restricoes = n_restricoes # Número de restrições
        self.c = coefs_funcao_objetivo # Lista de cada coeficiente da função objetivo. Ex.: Z = 5A + 3B coefs_funcao_objetivo = [5, 3]
        self.A = coefs_restricoes # Lista de cada coeficiente das restrições. Ex.: 10A + 3B < 30; 13A + 12B >= 55; 32A + 9B >= 78 coefs_restricoes = [10, 3, 13, 12, 32, 9]
        self.b = lados_direitos  # Lista de cada coeficiente de restrição do Lado Direito da equação. Ex.: 10A + 3B < 30; 13A + 12B >= 55; 32A + 9B >= 78 lados_direitos = [30, 55, 78]
        self.sinais = sinais # Indica se o sinal é maior igual ou menor de cada equação das restrições. Ex.: Ex.: 10A + 3B < 30; 13A + 12B >= 55; 32A + 9B >= 78 sinais = ['less', 'greater', 'greater']

        self.list_to_array()

    # Desembrulhar List de restrições em Array de Lists
    def list_to_array(self):
        restricoes_array = []  # Initialize as an empty list
        for i in range(self.n_restricoes):
            # Initialize the sublist for each row
            row_list = []
            for j in range(self.n_var):
                row_list.append(self.A[j + i * self.n_var])  # Adjust the index to get the correct coefficient
            restricoes_array.append(row_list)

        self.A = restricoes_array
        print(f'Array de restrições (A): {self.A}')


    # Função para realizar operações de pivoteamento na tabela simplex.
    def pivot_on(self, tableau, row, col):
        nr, nc = tableau.shape  # Obtém o número de linhas (nr) e colunas (nc) do tableau.
        pivot = tableau[row, col]  # Elemento de pivô.
        tableau[row, :] /= pivot  # Transforma o elemento de pivô em 1 dividindo toda a linha por ele.
        for r in range(nr):  # Para cada linha no tableau...
            if r == row:  # Exceto a linha do pivô...
                continue
            # Subtrai um múltiplo da linha do pivô para zerar o elemento na coluna do pivô.
            tableau[r, :] -= tableau[r, col] * tableau[row, :]

    # Função principal do método simplex.
    def simplex(self):
        if not self.tipo_problema:  # Se o problema é de minimização...
            self.c = -self.c  # Inverte os sinais dos coeficientes da função objetivo.
            
        # Construção do tableau inicial.
        self.A = np.hstack((self.A, np.eye(len(self.A))))  # Adiciona as variáveis de folga à matriz de restrições A.
        self.c = np.concatenate((self.c, np.zeros(len(self.A))))  # Adiciona zeros correspondentes às variáveis de folga na função objetivo.
        tableau = np.vstack((self.A, self.c))  # Combina A e c para formar o tableau.
        self.b = np.concatenate((self.b, [0]))  # Adiciona o lado direito das restrições e o valor da função objetivo (0) ao tableau.
        tableau = np.column_stack((tableau, self.b))  # Adiciona a coluna do lado direito ao tableau.

        # Processo iterativo do método simplex.
        while (self.tipo_problema and np.any(tableau[-1, :-1] < 0)) or (not self.tipo_problema and np.any(tableau[-1, :-1] > 0)):
            # Escolha da coluna do pivô (coluna de entrada).
            if self.tipo_problema:
                col = np.argmin(tableau[-1, :-1])  # Para maximização: escolhe o menor valor negativo na linha da função objetivo.
            else:
                col = np.argmax(tableau[-1, :-1])  # Para minimização: escolhe o maior valor na linha da função objetivo.
            # Se todos os elementos na coluna do pivô são ≤ 0, então o problema é ilimitado (sem solução ótima).
            if np.all(tableau[:, col] <= 0):
                raise ValueError("Problema sem solução.")
            # Escolha da linha do pivô (linha de saída).
            ratios = tableau[:-1, -1] / tableau[:-1, col]  # Calcular as razões entre o lado direito e os elementos da coluna do pivô.
            row = np.argmin(np.where(tableau[:-1, col] > 0, ratios, np.inf))  # A linha do pivô é a que tem o menor valor positivo na razão.
            self.pivot_on(tableau, row, col)  # Realiza a operação de pivoteamento.

        # Após concluir as iterações, os preços sombra podem ser encontrados na última linha do tableau (negativos para maximização).
        shadow_prices = -tableau[-1, len(self.c)-len(self.A):len(self.c)]  # Apenas os preços sombra das restrições originais.
        
        return tableau, shadow_prices