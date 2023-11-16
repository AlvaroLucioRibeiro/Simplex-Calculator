from typing import Dict, List

class Simplex():
    # Setup Simplex
    def __init__(self, tipo_problema, n_var, n_restricoes, coefs_funcao_objetivo, coefs_restricoes, lados_direitos) -> None:
        self.tipo_problema: str = tipo_problema # "max" or "min"
        self.n_var: int = n_var
        self.n_restricoes: int = n_restricoes
        self.coefs_funcao_objetivo: float = coefs_funcao_objetivo
        self.coefs_restricoes: float = coefs_restricoes
        self.lados_direitos: float = lados_direitos

    # Calculate the optimal result from something like this: Z = coef1*A + coef2*B + ...
    def calcular_preco_otimo(self) -> List[float]:
        pass # Returns something like this: [optimal_value_var1, optimal_value_var2, optimal_value_var3, optimal_result]

    def calcular_precos_sombra(self) -> Dict[str: float]:
        pass # Retuns something like this: {"shadow_price_coef1": new_value_objective_function1, "shadow_price_coef2": new_value_objective_function2, "shadow_price_coef3": new_value_objective_function3, "shadow_price_coef4": new_value_objective_function4}