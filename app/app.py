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
    # Então retornar o template de resultado final do PPL
    # OBS.: Criei uma lógica básica aqui, mas não sei se funciona, é para te dar um norte sobre o papel que esta rota deve fazer...
    coefs = []
    for coef in request['coeficientes']:
        coefs.append(coef)

    return redirect(url_for('result'), coefs=coefs)

if __name__ == '__main__':
    app.run(debug=True)
