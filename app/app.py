from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/ppl/setup', methods=['GET', 'POST'])
def ppl_setup():
    # Ao clicar em continuar, depois da config. inicial do PPL
    if request.method == 'POST':
        num_variaveis = int(request.form['num_variaveis'])
        tipo_problema = request.form['tipo_problema']
        num_restricoes = int(request.form['num_restricoes'])

        # Redireciona para outra rota
        return render_template('modelo-ppl.html', num_variaveis=num_variaveis, tipo_problema=tipo_problema, num_restricoes=num_restricoes)

    return render_template('index.html')

# Ao clicar para obter o resultado final do PPL
@app.route('/ppl/evaluate', methods=['POST'])
def evaluate():
    # Realizar operações necessárias com os coeficientes recebidos do usuário
    # Então retornar o template de resultado final do PPL, com ponto ótimo, lucro ótimo e o preço-sombra de cada restrição

    #print(f'keys: {len(request.form.keys())}')
    #print(f'form: {request.form}')
    '''
    ([('coef_objetivo0', '8'), ('coef_objetivo1', '9'), ('coef_restricao00', '10'), ('coef_restricao01', '11'), ('lado_direito0', '12'), ('coef_restricao10', '13'), ('coef_restricao11', '14'), ('lado_direito1', '15'), ('coef_restricao20', '16'), ('coef_restricao21', '17'), ('lado_direito2', '18'), ('coef_restricao30', '19'), ('coef_restricao31', '20'), ('lado_direito3', '21'), ('coef_restricao40', '22'), ('coef_restricao41', '23'), ('lado_direito4', '24')])


    ([('coef_objetivo0', '30'), ('coef_objetivo1', '64'), ('lado_direito_fo', '550'), ('coef_restricao00', '10'), ('coef_restricao01', '11'), ('lado_direito0', '15'), ('coef_restricao10', '21'), ('coef_restricao11', '32'), ('lado_direito1', '44')])
    '''
    data = dict(request.form)
    print(data)

    # Initialize lists to store coefficients
    coefs_func_objetivo = []
    coefs_restricao = []
    lados_direitos = []

    # Extrair tamanho do request
    for key, value in data:
        # Obter coeficientes da Função Objetivo
        if key.startswith('coef_objetivo'):
            coefs_func_objetivo.append(float(value))
        
        # Obter coeficientes de cada restrição
        elif key.startswith('coef_restricao'):
            # Extract the indices from the key
            _, restricao_index, coef_index = key.split('_')
            restricao_index = int(restricao_index)
            coef_index = int(coef_index)

            # Make sure the lists are long enough
            while len(coefs_restricao) <= restricao_index:
                coefs_restricao.append([])
                lados_direitos.append([])

            # Append the coefficient to the appropriate list
            coefs_restricao[restricao_index].append(float(value))

        # Obter lado direito de cada restrição
        elif key.startswith('lado_direito'):
            # Extract the index from the key
            _, restricao_index = key.split('_')
            restricao_index = int(restricao_index)

            # Make sure the lists are long enough
            while len(lados_direitos) <= restricao_index:
                coefs_restricao.append([])
                lados_direitos.append([])

            # Append the right-hand side value to the appropriate list
            lados_direitos[restricao_index].append(float(value))


    # Calcular o resultado


    # Envelopamento do resultado de cada var e do preco-sombra de cada var
    results = {}

    # Valores Ótimos
    vars = []

    # Preços sombra p/ cada var
    precos_sombra = []

    results['vars'] = vars
    results['precos_sombra'] = precos_sombra

    return render_template('success.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
