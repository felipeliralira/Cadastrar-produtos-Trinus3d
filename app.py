from flask import Flask, render_template, request
import requests

app = Flask(__name__)


# ============================================================
# CONFIGURAÇÃO DO GOOGLE PLANILHAS
# ============================================================

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyunPOLlqG6rd3SggPT8G5FM1vmsYMJBHdi-mrKtIdmfFT5MHPHy3SAckve8VfnTHoImg/exec"


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

        # ========================================================
        # RECEBE OS DESTINOS SELECIONADOS
        # ========================================================

        # Agora pode receber vários destinos
        destinos = request.form.getlist("destinos")

        # Remove espaços desnecessários
        destinos = [destino.strip() for destino in destinos]


        # ========================================================
        # RECEBE OS DADOS DO PRODUTO
        # ========================================================

        nome = request.form.get("nome", "").strip()
        custo_adc = request.form.get("custo_adc", "").strip()
        custo = request.form.get("custo", "").strip()
        atacado = request.form.get("atacado", "").strip()
        varejo = request.form.get("varejo", "").strip()
        pedido_minimo = request.form.get("pedido_minimo", "").strip()


        # ========================================================
        # ABAS PERMITIDAS
        # ========================================================

        abas_permitidas = [
            "Produtos All",
            "Shopee/TikTok",
            "Mercado Livre/ Site"
        ]


        # ========================================================
        # VERIFICA SE PELO MENOS UMA ABA FOI SELECIONADA
        # ========================================================

        if not destinos:
            return "Erro: selecione pelo menos um local para cadastrar o produto."


        # ========================================================
        # VERIFICA SE OS DESTINOS SÃO VÁLIDOS
        # ========================================================

        for destino in destinos:

            if destino not in abas_permitidas:
                return f"Erro: destino inválido: {destino}"


        # ========================================================
        # VERIFICA O NOME
        # ========================================================

        if not nome:
            return "Erro: o nome do produto é obrigatório."


        # ========================================================
        # DADOS QUE SERÃO ENVIADOS PARA O GOOGLE PLANILHAS
        # ========================================================

        dados = {
            "destinos": destinos,
            "nome": nome,
            "custo_adc": custo_adc,
            "custo": custo,
            "atacado": atacado,
            "varejo": varejo,
            "pedido_minimo": pedido_minimo
        }


        # ========================================================
        # ENVIA OS DADOS PARA O GOOGLE APPS SCRIPT
        # ========================================================

        resposta = requests.post(
            GOOGLE_SCRIPT_URL,
            json=dados,
            timeout=10
        )


        # ========================================================
        # VERIFICA RESPOSTA DO GOOGLE
        # ========================================================

        if resposta.status_code != 200:
            return f"Erro ao enviar para o Google Planilhas: {resposta.text}"


        # ========================================================
        # PÁGINA DE SUCESSO
        # ========================================================

        return render_template(
            "sucesso.html",
            nome_produto=nome
        )


    # ============================================================
    # ERRO DE CONEXÃO
    # ============================================================

    except requests.exceptions.RequestException as err:

        return f"Erro de conexão com o Google Planilhas: {err}"


    # ============================================================
    # OUTROS ERROS
    # ============================================================

    except Exception as err:

        return f"Erro ao cadastrar produto: {err}"


# ============================================================
# INICIAR SERVIDOR
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)
