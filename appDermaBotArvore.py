from flask import Flask, request, jsonify, render_template, session as sessao
from uuid import uuid4
import json
import re

from motorArvore import proxima_etapa, registrar_resposta, reiniciar_sessao
from arvoreDecisao import ARVORE_DECISAO
from telegram import TelegramSender, TelegramMessage 
from database import GerenciadorEstadoDB


from telegram import Telegram_voicepath
import whisper

aplicativo = Flask(__name__, template_folder='.')
aplicativo.secret_key = "dermabot-desenvolvimento-arvore"

# Estado em memória por usuário (chaveado por id na sessão Flask)
# sessoes_usuarios = {}

aplicativo.config.update(
    SESSION_COOKIE_SECURE=True,      # só envia em HTTPS (Render é https)
    SESSION_COOKIE_SAMESITE="Lax" 
)


db_estado = GerenciadorEstadoDB()
telegram_sender = TelegramSender()

### TODO Eliminar essas funcoes

def obter_estado(id_usuario: str):
    """ Obtém o estado (JSON) do usuário a partir do banco de dados. """
    # Garante que a sessão exista e retorna o estado salvo
    sessao = db_estado.obter_ou_criar_sessao(id_usuario)
    return json.loads(sessao['estado'])

def salvar_estado(id_usuario: str, est: dict):
    """ Salva o estado (JSON) do usuário no banco de dados. """
    db_estado.salvar_estado_json(id_usuario, json.dumps(est))

def reiniciar_sessao_local(id_usuario: str):
    """ 
    Reinicia a sessão no banco de dados (estado e status).
    Retorna o novo estado (dict).
    """
    return db_estado.reiniciar_sessao_completa(id_usuario)


class mensagem:
    boas_vindas = """
    Olá! Eu sou o DermaBot! Estou aqui para te ajudar a diagnosticar as principais doenças dermatológicas e a dar orientações sobre elas. Seja bem-vinda(o)!
    Deseja iniciar o pré-diagnóstico?
    1 - Sim
    2 - Sair
    """
    voz = "Muito em breve você vai poder conversar por voz comigo, mas por enquanto podemos conversar por texto?"
    invalida = "Desculpe, eu ainda não consigo entender este tipo de mensagem. Você pode falar comigo por texto?" 
    sair = "Obrigado por utilizar o DermaBot! A conversa foi encerrada.\n\nPara recomeçar, envie 'Olá'."
    recomecar = "Gostaria de iniciar o pré-diagnóstico? Por favor, responda:\n1 - Sim\n2 - Sair"
    
mensagem = mensagem()
    
def perguntar_proximo_no(estado, id_usuario: str):
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
        salvar_estado(id_usuario, estado)

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

    return "Eita! Algo deu errado! Desculpe-me! Digite 1 para reiniciar ou 2 para sair.", True



@aplicativo.route("/")
def pagina_inicial():
    if "id_usuario_dermabot" not in sessao:
        sessao["id_usuario_dermabot"] = "web_" + str(uuid4())
    return render_template("index.html")


@aplicativo.route("/health")
def saude():
    return "ok", 200


@aplicativo.route("/webhook", methods=["POST"])
def webhook_telegram():
    """
    Webhook para o telegram.
    """
    corpo = request.get_json(silent=True) or {}
    print(corpo)
    try:
        dados_telegram = TelegramMessage.model_validate(corpo)
    except Exception as e:
        print(f"Erro ao validar payload do Telegram: {e}")
        return jsonify({"status": "erro", "msg": "payload invalido"}), 400
    
    chat_id = dados_telegram.message.chat.id
    
    if dados_telegram.message.voice is not None:

        model = whisper.load_model("base")
        # Transcribe an audio file
        result = model.transcribe(Telegram_voicepath(dados_telegram.message.voice.file_id), language="pt")
        #telegram_sender.send_message(chat_id, mensagem.voz)
        telegram_sender.send_message(chat_id, f" Você respondeu **{result['text']}** por voz")
        mensagem_recebida = result['text']
        
    elif not dados_telegram.message or not dados_telegram.message.chat or not dados_telegram.message.text:

        telegram_sender.send_message(chat_id, mensagem.invalida)
        return jsonify({"status": "ok", "msg": mensagem.invalida}), 200
    else:
        mensagem_recebida = re.sub('[^\\w]' , ' ', dados_telegram.message.text).strip() #remover tudo que não for alfanumérico, emojii e pontuação são removidos
    
    mensagem_recebida = mensagem_recebida.strip().lower()
    id_usuario = str(chat_id) 
    
    if not mensagem_recebida:
        telegram_sender.send_message(chat_id, mensagem.invalida)
        return jsonify({"status": "ok", "msg": mensagem.invalida}), 200

    # Coleta dados do usuário do Telegram
    user_data = {
        "first_name": dados_telegram.message.chat.first_name,
        "last_name": dados_telegram.message.chat.last_name,
        "username": dados_telegram.message.chat.username
    }
    
    # 1. Log da mensagem recebida
    db_estado.log_historico(id_usuario, 'RECEBIDO', mensagem_recebida)

    # 2. Obter ou Criar Sessão (sempre atualiza dados do usuário)
    sessao_db = db_estado.obter_ou_criar_sessao(id_usuario, user_data)
    estado = json.loads(sessao_db['estado'])
    status_sessao = sessao_db['status_sessao']

    texto_resposta = None
    triggers_reinicio = {"olá", "oi", "recomeçar"}

    # 3. Verificar gatilhos de reinício (prioridade máxima)
    if mensagem_recebida in triggers_reinicio:
        estado = reiniciar_sessao_local(id_usuario) # Reseta estado e status para 'MENU'
        texto_resposta = mensagem.boas_vindas
        status_sessao = 'MENU' # Atualiza status local
    
    # 4. Processar com base no status da sessão
    elif status_sessao == 'MENU':
        if mensagem_recebida in {"1", "sim", "s", "yes", "claro", "bora", "comecar", "começar"}:
            # Inicia árvore
            estado = reiniciar_sessao_local(id_usuario) # Limpa respostas
            db_estado.mudar_status_sessao(id_usuario, 'ATIVO') # Define status 'ATIVO'
            
            texto_resposta, terminou = perguntar_proximo_no(estado, id_usuario)
            
            if terminou: # Se terminou imediatamente (ex: erro na árvore)
                reiniciar_sessao_local(id_usuario) # Volta ao 'MENU'

        elif mensagem_recebida in {"2", "sair", "encerrar", "finalizar", "fim", "não", "nao", "n", "no"}:
            texto_resposta = mensagem.sair
            # Status permanece 'MENU'

        else:
            # Entrada inválida no menu
            texto_resposta = mensagem.recomecar
            # Status permanece 'MENU'

    elif status_sessao == 'ATIVO':
        # Processamento normal dentro da árvore de decisão
        
        # (Verificação de 'reiniciar' na árvore já não é mais necessária,
        # pois os gatilhos 'olá', 'oi', 'recomeçar' são tratados primeiro)
        
        if estado.get("pergunta_atual"):
            registrar_resposta(estado, mensagem_recebida)
            # Salva o progresso (estado JSON)
            salvar_estado(id_usuario, estado) 
        
        # Avança para o próximo nó
        texto_resposta, terminou = perguntar_proximo_no(estado, id_usuario)

        if terminou:
            # Diagnóstico concluído, volta ao menu
            estado = reiniciar_sessao_local(id_usuario) # Define status='MENU'

    # 5. Enviar resposta e logar
    if texto_resposta:
        try:
            db_estado.log_historico(id_usuario, 'ENVIADO', texto_resposta)
            telegram_sender.send_message(chat_id, texto_resposta)
        except Exception as e:
            print(f"Erro ao enviar mensagem para {chat_id}: {e}")
            # Tenta logar a falha
            db_estado.log_historico(id_usuario, 'ERRO_ENVIO', str(e))
    else:
        # Caso nenhuma lógica tenha gerado resposta (improvável)
        print(f"Nenhuma resposta gerada para {id_usuario} (msg: '{mensagem_recebida}')")

    return jsonify({"status": "ok", "msg": texto_resposta}), 200

if __name__ == "__main__":
    print("Iniciando DermaBot ...")
    aplicativo.run(host="0.0.0.0", port=5000, debug=False)