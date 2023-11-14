from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/ppl/setup', methods=['GET', 'POST'])
def ppl_setup():
    # Ao clicar em continuar, depois da config. inicial do PPL
    if request.method == 'POST':
        #print(request.form)
        #ImmutableMultiDict([('num_variaveis', '2'), ('tipo_problema', 'max'), ('num_restricoes', '5')])

        global num_variaveis
        global num_restricoes
        num_variaveis = int(request.form['num_variaveis'])
        num_restricoes = int(request.form['num_restricoes'])

        # Redireciona para outra rota
        return render_template('modelo-ppl.html', num_variaveis=num_variaveis, num_restricoes=num_restricoes)

    return render_template('index.html')

# Ao clicar para obter o resultado final do PPL
@app.route('/ppl/evaluate', methods=['POST'])
def evaluate():
    # Realizar operações necessárias com os coeficientes recebidos do usuário
    # Então retornar o template de resultado final do PPL, com ponto ótimo, lucro ótimo e o preço-sombra de cada restrição

    #print(f'keys: {len(request.form.keys())}')
    #print(f'form: {request.form}')
    '''
    {'coef_objetivo0': '200', 'coef_objetivo1': '300', 'lado_direito_fo': '4000', 'coef_restricao00': '50', 'coef_restricao01': '60', 'lado_direito_0': '70', 'coef_restricao10': '80', 'coef_restricao11': '90', 'lado_direito_1': '100', 'coef_restricao20': '110', 'coef_restricao21': '120', 'lado_direito_2': '130', 'tipo_problema': 'max'}
    Tipo Problema: max
    Num. Variáveis: 2
    Num. Restrições: 3
    Coefs Objetivo: [200.0, 300.0]
    Coefs Restrições: [50.0, 60.0, 80.0, 90.0, 110.0, 120.0]
    Lados Direitos: [4000.0, 70.0, 100.0, 130.0]
    '''

    data = dict(request.form)
    print(data)

    # Initialize lists to store coefficients
    tipo_problema = data['tipo_problema']
    coefs_func_objetivo = []
    coefs_restricao = []
    lados_direitos = []

    # Extrair componentes do request
    for key, value in data.items():
        if key.startswith('coef_objetivo'):
            coefs_func_objetivo.append(float(value))
        elif key.startswith('coef_restricao'):
            coefs_restricao.append(float(value))
        elif key.startswith('lado_direito'):
            lados_direitos.append(float(value))
    
    
    print(f'Tipo Problema: {tipo_problema}')
    print(f'Num. Variáveis: {num_variaveis}')
    print(f'Num. Restrições: {num_restricoes}')
    print(f'Coefs Objetivo: {coefs_func_objetivo}')
    print(f'Coefs Restrições: {coefs_restricao}')
    print(f'Lados Direitos: {lados_direitos}') # Primeiro elemento é o lado direito da F.O.

    # Calcular o resultado


    # Valores Ótimos
    vars = []

    # Preços sombra p/ cada var
    precos_sombra = []

    # Envelopamento do resultado de cada var e do preco-sombra de cada var
    results = {}

    results['vars'] = vars
    results['precos_sombra'] = precos_sombra

    return render_template('success.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
