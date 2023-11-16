from typing import Dict, List
import numpy as np

class Simplex():
    # Simplex Setup
    def __init__(self, tipo_problema, n_var, n_restricoes, coefs_funcao_objetivo, coefs_restricoes, lados_direitos, sinais) -> None:
        self.tipo_problema: str = tipo_problema # "max" or "min"
        self.n_var: int = n_var
        self.n_restricoes: int = n_restricoes
        self.coefs_funcao_objetivo: float = coefs_funcao_objetivo
        self.coefs_restricoes: float = coefs_restricoes
        self.lados_direitos: float = lados_direitos
        self.sinais = sinais # Indica se é maior igual ou menor igual o sinal de cada restrição. Ex.: ['greater', 'less', 'less', ...]

    def simplex(self):
        # Adiciona variáveis de folga e excedente ao sistema de equações
        A1 = np.hstack([self.coefs_restricoes, np.eye(len(self.lados_direitos))])
        A2 = np.hstack([-np.eye(len(self.lados_direitos)), np.eye(len(self.lados_direitos))])
        A = np.vstack([A1, A2])

        c = np.hstack([self.coefs_funcao_objetivo, np.zeros(2 * len(self.lados_direitos))])

        # Adiciona as variáveis de folga e excedente à matriz de coeficientes com os sinais
        for i, sinal in enumerate(self.sinais):
            if sinal == 'less':
                A[i, :] *= -1
            elif sinal == 'equal':
                A[i, :] *= 0  # Restrição igual vira duas desigualdades

        tableau = np.vstack([np.hstack([A, np.array(self.lados_direitos).reshape(-1, 1)]), np.hstack([c, 0])])

        while np.any(tableau[-1, :-1] < 0):
            # Escolhe a coluna pivot (menor coeficiente na linha objetivo)
            pivot_col = np.argmin(tableau[-1, :-1])

            # Escolhe a linha pivot (menor razão entre b e a coluna pivot)
            pivot_row = np.argmin(tableau[:-1, -1] / tableau[:-1, pivot_col])

            # Atualiza o tableau usando a regra do pivô
            tableau[pivot_row, :] /= tableau[pivot_row, pivot_col]
            for i in range(tableau.shape[0]):
                if i != pivot_row:
                    tableau[i, :] -= tableau[i, pivot_col] * tableau[pivot_row, :]

        # Extrai os valores ótimos e o preço sombra
        optimal_values = tableau[-1, :-1]
        shadow_prices = tableau[:-1, -1]

        return optimal_values, shadow_prices
    
    # Calculate the optimal result from something like this: Z = coef1*A + coef2*B + ...
    def calcular_preco_otimo(self) -> List[float]:
        pass # Returns something like this: [optimal_value_var1, optimal_value_var2, optimal_value_var3, optimal_result]

    # Calculate the shadow-price for each constraint equation
    def calcular_precos_sombra(self) -> Dict:
        pass # Retuns something like this: {"shadow_price_coef1": new_value_objective_function1, "shadow_price_coef2": new_value_objective_function2, "shadow_price_coef3": new_value_objective_function3, "shadow_price_coef4": new_value_objective_function4}