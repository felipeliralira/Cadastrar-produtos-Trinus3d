from flask import Flask, render_template, redirect, url_for, request
import requests

app = Flask(__name__)

# ============================================================
# CONFIGURAÇÃO DO GOOGLE PLANILHAS
# ============================================================

# Depois vamos colocar aqui a URL do seu Google Apps Script
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2rK0W-E3hwfmo-raL_lR9fN9SDYrgMld36QB5hU_wYxvCBsJU9P9PrV48tmfw4aFS9w/exec"


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# FORMULÁRIO DE CADASTRO
# ============================================================

@app.route("/formulario")
def exibirFormulario():
    return render_template("cadastro.html")


# ============================================================
# CADASTRAR PRODUTO
# ============================================================

@app.route("/cadastrar", methods=["POST"])
def criarCadastro():

    try:
        # Recebe os dados enviados pelo formulário
        destino = request.form.get("destino", "").strip()
        nome = request.form.get("nome", "").strip()
        custo_adc = request.form.get("custo_adc", "").strip()
        custo = request.form.get("custo", "").strip()
        atacado = request.form.get("atacado", "").strip()
        varejo = request.form.get("varejo", "").strip()
        pedido_minimo = request.form.get("pedido_minimo", "").strip()

        # Verifica se o destino foi selecionado
        if not destino:
            return "Erro: selecione onde o produto será cadastrado."

        # Verifica se o nome foi preenchido
        if not nome:
            return "Erro: o nome do produto é obrigatório."

        # Dados que serão enviados para o Google Planilhas
        dados = {
            "destino": destino,
            "nome": nome,
            "custo_adc": custo_adc,
            "custo": custo,
            "atacado": atacado,
            "varejo": varejo,
            "pedido_minimo": pedido_minimo
        }

        # Envia os dados para o Google Apps Script
        resposta = requests.post(
            GOOGLE_SCRIPT_URL,
            json=dados,
            timeout=10
        )

        # Verifica resposta do Google
        if resposta.status_code != 200:
            return f"Erro ao enviar para o Google Planilhas: {resposta.text}"

        # Página de sucesso
        return render_template(
            "sucesso.html",
            nome_produto=nome
        )

    except requests.exceptions.RequestException as err:
        return f"Erro de conexão com o Google Planilhas: {err}"

    except Exception as err:
        return f"Erro ao cadastrar produto: {err}"


# ============================================================
# INICIAR SERVIDOR
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)