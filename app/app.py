from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Ao clicar em continuar, depois da config. inicial do PPL
@app.route('/ppl/setup', methods=['GET', 'POST'])
def ppl_setup():
    if request.method == 'POST':
        num_variaveis = int(request.form['num_variaveis'])
        tipo_problema = request.form['tipo_problema']
        num_restricoes = int(request.form['num_restricoes'])

        # Redireciona para outra rota ou renderiza outra página
        return redirect(url_for('modelo-ppl', num_variaveis=num_variaveis, tipo_problema=tipo_problema, num_restricoes=num_restricoes))

    return render_template('ppl_setup.html')

# Ao clicar para obter o resultado final do PPL
@app.route('/ppl/evaluate', methods=['POST'])
def evaluate():
    # Realizar operações necessárias com os coeficientes recebidos do usuário
    # Então retornar o template de resultado final do PPL, com ponto ótimo, lucro ótimo e o preço-sombra de cada restrição
    # OBS.: Criei uma lógica básica aqui, mas não sei se funciona, é para te dar um norte sobre o papel que esta rota deve fazer...

    # Envelopamento do resultado de cada var e do preco-sombra de cada var
    results = {}

    # Valores Ótimos
    vars = []
    for var in request['variaveis']:
        vars.append(var)

    # Preços sombra p/ cada var
    precos_sombra = []
    for ps in request['precos_sombra']:
        precos_sombra.append(ps)

    results['vars'] = vars
    results['precos_sombra'] = precos_sombra

    return redirect(url_for('result'), results=results)

if __name__ == '__main__':
    app.run(debug=True)
