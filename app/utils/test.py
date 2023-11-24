import numpy as np

class Simplex():
    def __init__(self, coefs_funcao_objetivo, coefs_restricoes, lados_direitos, sinais) -> None:
        self.n_var = len(coefs_funcao_objetivo)
        self.n_restricoes = len(coefs_restricoes)
        self.c = coefs_funcao_objetivo
        self.A = coefs_restricoes
        self.b = lados_direitos
        self.sinais = sinais

    def create_tableau(self):
        # Create header row
        header_row = [None] + [f"var{i+1}" for i in range(self.n_var)] + [f"x{i+1}" for i in range(self.n_restricoes)] + ["right_side"]

        # Create tableau with header row
        self.tableau = [header_row]

        # Create objective function row
        obj_row = ["Z"] + [-coef for coef in self.c] + [0] * (self.n_restricoes + 1)
        self.tableau.append(obj_row)

        # Create constraint rows
        for i in range(self.n_restricoes):
            constraint_row = [f"x{i+1}"] + self.A[i] + [0] * i + [1] + [0] * (self.n_restricoes - i - 1) + [self.b[i]]
            if self.sinais[i] == 'greater':
                # If the constraint is greater, negate the slack variable
                constraint_row[self.n_var + i + 1] *= -1
            self.tableau.append(constraint_row)

        self.tableau = np.array(self.tableau)

        print(f"Tableau in iteration 0: \n{self.tableau}")
    
    def pivot_column(self):
        # Find the column index with the most negative coefficient in the "Z" row
        pivot_col = np.argmin(self.tableau[1, 1:]) + 1  # Adds 1 because the string column

        if np.all(self.tableau[1:, pivot_col] <= 0):
            raise ValueError("Problema sem solução.")
        
        return pivot_col

    def pivot_row(self, pivot_col_index):
        # Calculate the ratios of the right-hand side values to the coefficients in the pivot column
        right_side = self.tableau[2:, -1]
        pivot_column = self.tableau[2:, pivot_col_index]
        ratios = []

        index = 0
        for i in pivot_column: 
            if i > 0:
                ratios.append(float(right_side[index] / pivot_column[index])) # Razões
            else:
                ratios.append(-1)

            index += 1

        ratios = np.array(ratios)
        print(ratios)

        positive_ratios = np.where(ratios > 0)[0]

        # Find the index of the smallest positive element
        if len(positive_ratios) > 0:
            index_of_smallest_positive = positive_ratios[np.argmin(ratios[positive_ratios])]
            pivot_row_index = index_of_smallest_positive + 2

            return pivot_row_index
        else:
            raise("No positive elements in the array.")


    def start_simplex(self):
        iteration = 0
        while np.any(self.tableau[1, 1:] < 0):
            # Find the pivot element
            col = self.pivot_column()
            row = self.pivot_row(col)
            self.pivot = self.tableau[row, col]
            print(f"Pivot Row: {row}. \nPivot Column: {col}. \nPivot: {self.pivot}")

            # Divide the new pivot row by the pivot
            self.new_pivot_row = np.zeros(len(self.tableau[row, 1:]))
            for index, value in enumerate(self.tableau[row, 1:]):
                self.new_pivot_row[index] = float(value / self.pivot)

            print(f"New Pivot Row: {self.new_pivot_row}")

            # Swap the header and column names
            column_to_row = self.tableau[0, col]
            self.tableau[0, col] = self.tableau[row, 0]
            self.tableau[row, 0] = column_to_row

            # Old pivot column
            self.old_pivot_column = self.tableau[1:, col].astype(float)
            print(f"Old Pivot Column: {self.old_pivot_column}")

            # Fill the remaining tableau row with the NEW values (-Cp*Lp' + Ln)
            for row_index, row_tableau in enumerate(self.tableau[1:, 1:]):
                for col_index, col_value in enumerate(row_tableau):
                    '''print(f"Tableau Element: {self.tableau[row_index + 1, col_index + 1]}")
                    print(f"Old Pivot Column Element: {self.old_pivot_column[row_index]}")
                    print(f"New Pivot Row Element: {self.new_pivot_row[col_index]}")'''
                    # Checking if it's not the pivot row
                    if((row_index + 1) != row):
                        self.tableau[row_index + 1, col_index + 1] = ((-1.0)*self.old_pivot_column[row_index]*self.new_pivot_row[col_index]) + col_value


            # Add the new pivot row to the tableau
            self.tableau[row, 1:] = self.new_pivot_row

            # Keep track of the iteration
            iteration += 1

            print(f"Tableau in iteration {iteration}: {self.tableau}")

    def get_results(self):
        self.create_tableau()
        self.start_simplex()
        # Find optimal profit and optimal values
        optimal_profit = self.tableau[1, -1]


        optimal_values = {}
        for i in range(self.n_var):
            optimal_values[f"var{i+1}"] = 0.0
        
        print(optimal_values)

        for row in self.tableau[2:, :]:
            for key, value in optimal_values.items():
                if row[0] == key:
                    optimal_values[key] = row[-1]
        
        # Add zero to variables that are not in the correct position in the tableau, because they're equal to zero
        while(len(optimal_values) < self.n_var):
            for key, value in optimal_values:
                if value == 0:
                    optimal_values[key] = 0.0

        # Find shadow-prices
        shadow_prices = []
        row = self.tableau[1][1:-1]
        shadow_prices = row[-self.n_restricoes:]

        return optimal_profit, optimal_values, shadow_prices


# Example usage:
simplex_instance = Simplex(
    coefs_funcao_objetivo=[20, 60],
    coefs_restricoes=[[70, 70], [90, 50], [2, 0], [0, 3]],
    lados_direitos=[4900, 4500, 80, 180],
    sinais=['less', 'less', 'greater', 'greater']
)


'''
simplex_instance = Simplex(
    coefs_funcao_objetivo=[6, 4, 6, 8],
    coefs_restricoes=[[3,2,2,4], [1,1,2,3], [2,1,2,1], [1,0,0,0], [0,1,1,0], [0,0,0,1]],
    lados_direitos=[480,400,400,50,100,25],
    sinais=['less', 'less', 'less', 'greater', 'greater', 'less']
)
# RESULTADO CORRETO: $1250 -> (50, 0, 145, 10)
'''

optimal_profit, optimal_values, shadow_prices = simplex_instance.get_results()
print(f"Optimal Profit: {optimal_profit}")
print(f"Optimal Values: {optimal_values}")
print(f"Shadow Prices: {shadow_prices}")
