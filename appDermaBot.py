
from flask import Flask, request, jsonify, render_template, render_template_string, session as sessao
from uuid import uuid4

from motorArvore import proxima_etapa, registrar_resposta, reiniciar_sessao
from arvoreDecisao import ARVORE_DECISAO
from telegram import TelegramMessage, TelegramSender

aplicativo = Flask(__name__, template_folder='.')
aplicativo.secret_key = "dermabot-desenvolvimento-arvore"

# Estado em memória por usuário (chaveado por id na sessão Flask)
# sessoes_usuarios = {}

aplicativo.config.update(
    SESSION_COOKIE_SECURE=True,      # só envia em HTTPS (Render é https)
    SESSION_COOKIE_SAMESITE="Lax" 
)

def _estado_padrao():
    return {"etapa": "arvore", "respostas": {}, "pergunta_atual": None, "texto_pergunta_atual": None,
            "mostrou_inicio": False, "no_menu": True}

def obter_estado():
    est = sessao.get("estado")
    if not est:
        est = _estado_padrao()
        sessao["estado"] = est
    return est

def salvar_estado(est):
    sessao["estado"] = est



def mensagem_boas_vindas():
    return (
        "Olá! Eu sou o DermaBot! Estou aqui para te ajudar a diagnosticar as principais doenças dermatológicas e a dar orientações sobre elas. Seja bem-vinda(o)!\n\n"
        "Deseja iniciar o pré-diagnóstico?\n"
        "1 - Sim\n"
        "2 - Sair"
    )

def perguntar_proximo_no(estado):
    """
    Executa proxima_etapa e devolve (texto_resposta, terminou)
    - Se for pergunta: guarda 'pergunta_atual' na sessão e retorna o texto da pergunta.
    - Se for folha: retorna o diagnóstico/justificativas/orientações e indica que terminou.
    """
    respostas = estado.get("respostas", {})
    resultado = proxima_etapa(ARVORE_DECISAO, respostas)

    if "perguntar" in resultado:
        pergunta = resultado["perguntar"]["texto"]
        estado["pergunta_atual"] = resultado["perguntar"]["caracteristica"]
        estado["texto_pergunta_atual"] = pergunta
        salvar_estado(estado)
        return pergunta, False

    if "folha" in resultado:
        folha = resultado["folha"]
        dx = folha.get("dx", "Diagnóstico não definido")
        justific = folha.get("justificativa", [])
        orient = folha.get("orientacoes", [])

        txt = f"Diagnóstico sugerido: {dx}"
        if justific:
            txt += "\n\nPor quê:\n- " + "\n- ".join(justific)
        if orient:
            txt += "\n\nOrientações iniciais:\n- " + "\n- ".join(orient)
        txt += "\n\nDigite 1 para iniciar um novo caso ou 2 para sair."
        return txt, True

    # retorno de falha
    return "Eita! Algo deu errado! Desculpe-me! Digite 1 para reiniciar ou 2 para sair.", True

telegram = TelegramSender()

@aplicativo.route("/")
def pagina_inicial():
    if "id_usuario_dermabot" not in sessao:
        sessao["id_usuario_dermabot"] = str(uuid4())
    #return render_template_string(HTML_PAGINA_INICIAL)
    #return render_template('index.html')

@aplicativo.route("/saude")
def saude():
    return "ok", 200


@aplicativo.route("/conversa", methods=["POST"])
def conversar():
    if "id_usuario_dermabot" not in sessao:
        sessao["id_usuario_dermabot"] = str(uuid4())
    id_usuario = sessao["id_usuario_dermabot"]

    corpo = request.get_json(silent=True) or {}
    print(corpo)
    msg = TelegramMessage(**corpo)
    
    if msg.message.voice is not None:
        print('Olha Olha, recebemos uma mensagem de voz')
    elif msg.message.text is not None:
        mensagem_recebida = msg.message.text.strip().lower()
        chat_id = msg.message.chat.id 
        telegram.send_message(chat_id, mensagem_boas_vindas())
        
    #mensagem_recebida = (corpo.get("mensagem") or "").strip().lower()

    # Recupera/cria estado de sessão específico do usuário
    # estado = sessoes_usuarios.get(id_usuario)
    estado = obter_estado()
    if not estado:
        estado = reiniciar_sessao()
        estado["mostrou_inicio"] = False
        estado["no_menu"] = True
        #sessoes_usuarios[id_usuario] = estado
        salvar_estado(estado)

    respostas_usuario = []

    # Bootstrap da interface web
    if mensagem_recebida == "__bootstrap__":
        estado["mostrou_inicio"] = True
        estado["no_menu"] = True
        # sessoes_usuarios[id_usuario] = estado
        salvar_estado(estado)
        respostas_usuario.append(mensagem_boas_vindas())
        return jsonify({"respostas_usuario": respostas_usuario})

    # Primeira tela (boas-vindas)
    if not estado.get("mostrou_inicio", False):
        estado["mostrou_inicio"] = True
        estado["no_menu"] = True
        # sessoes_usuarios[id_usuario] = estado
        salvar_estado(estado)
        respostas_usuario.append(mensagem_boas_vindas())
        return jsonify({"respostas_usuario": respostas_usuario})

    # Lógica do menu inicial
    if estado.get("no_menu", False):
        if mensagem_recebida in {"1", "sim", "s", "yes", "claro", "bora", "comecar", "começar"}:
            # Inicia árvore
            estado = reiniciar_sessao()
            estado["mostrou_inicio"] = True
            estado["no_menu"] = False
            # sessoes_usuarios[id_usuario] = estado
            salvar_estado(estado)
            texto, terminou = perguntar_proximo_no(estado)
            respostas_usuario.append(texto)
            return jsonify({"respostas_usuario": respostas_usuario})

        if mensagem_recebida in {"2", "sair", "encerrar", "finalizar", "fim", "não", "nao", "n", "no"}:
            respostas_usuario.append("Obrigado por utilizar o DermaBot! A conversa foi encerrada.\n\nPara recomeçar, envie qualquer mensagem.")
            # Mantém no menu para poder reabrir com nova mensagem
            estado["pergunta_atual"] = None
            estado["no_menu"] = True
            # sessoes_usuarios[id_usuario] = estado
            salvar_estado(estado)
            return jsonify({"respostas_usuario": respostas_usuario})

        # Entrada inválida no menu
        respostas_usuario.append("Gostaria de iniciar o pré-diagnóstico? Por favor, responda:\n1 - Sim\n2 - Sair")
        return jsonify({"respostas_usuario": respostas_usuario})

    # Percorrendo a árvore de decisão (fora do menu)
    if mensagem_recebida in {"reiniciar", "recomeçar", "recomecar", "novo", "de novo", "reset"}:
        estado = reiniciar_sessao()
        estado["mostrou_inicio"] = True
        estado["no_menu"] = False
        # sessoes_usuarios[id_usuario] = estado
        salvar_estado(estado)
        texto, terminou = perguntar_proximo_no(estado)
        respostas_usuario.append(texto)
        return jsonify({"respostas_usuario": respostas_usuario})

    if estado.get("pergunta_atual"):
        registrar_resposta(estado, mensagem_recebida)
        # sessoes_usuarios[id_usuario] = estado
        salvar_estado(estado)

    # Avançar na árvore
    texto, terminou = perguntar_proximo_no(estado)
    respostas_usuario.append(texto)

    if terminou:
        # Após um diagnóstico, voltamos ao MENU (para que '2' volte a significar sair)
        estado = reiniciar_sessao()
        estado["mostrou_inicio"] = True
        estado["no_menu"] = True
        # sessoes_usuarios[id_usuario] = estado
        salvar_estado(estado)

    return jsonify({"respostas_usuario": respostas_usuario})


#if __name__ == "__main__":
    #aplicativo.run(port=5000, debug=True)

if __name__ == "__main__":
    # Execução local (dev)
    aplicativo.run(host="0.0.0.0", port=5000, debug=False)

