import sqlite3
import json
import atexit 


def _estado_padrao():
    """ Retorna o estado padrao"""
    return {"etapa": "arvore", "respostas": {}, "pergunta_atual": None, "texto_pergunta_atual": None,
            "mostrou_inicio": False, "no_menu": True}


class GerenciadorEstadoDB:
    """
    Classe separada para manipular o estado das sessões e o histórico 
    em um banco de dados SQLite.
    """
    def __init__(self, db_name="dermabot_sessoes.db"):
        self.db_name = db_name
        # check_same_thread=False é necessário para o Flask multithread
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.conn.row_factory = self.dict_factory # Retorna linhas como dicts
        self.criar_tabelas()
        self.criar_triggers()
        atexit.register(self.fechar_conexao) # Garante que a conexão feche ao sair

    def fechar_conexao(self):
        """ Fecha a conexão com o banco de dados. """
        if self.conn:
            self.conn.close()
            print("Conexão com SQLite fechada.")

    @staticmethod
    def dict_factory(cursor, row):
        """ Converte resultados da query (tuplas) em dicionários. """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def criar_tabelas(self):
        """ Garante que as tabelas de sessões e histórico existam. """
        cursor = self.conn.cursor()
        
        # Tabela de Sessões de Usuários
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessoes_usuarios (
            id_usuario TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            estado TEXT NOT NULL,
            status_sessao TEXT NOT NULL DEFAULT 'MENU',
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Tabela de Histórico de Conversa
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_conversa (
            id_historico INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario TEXT NOT NULL,
            direcao TEXT NOT NULL,
            mensagem TEXT,
            data_envio_recebimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_usuario) REFERENCES sessoes_usuarios (id_usuario)
        )
        """)
        self.conn.commit()

    def criar_triggers(self):
        """ Cria triggers para atualizar automaticamente a coluna data_alteracao. """
        cursor = self.conn.cursor()
        
        # Trigger para sessoes_usuarios
        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS trigger_sessoes_update
        AFTER UPDATE ON sessoes_usuarios
        FOR EACH ROW
        BEGIN
            UPDATE sessoes_usuarios 
            SET data_alteracao = CURRENT_TIMESTAMP 
            WHERE id_usuario = OLD.id_usuario;
        END;
        """)
        
        # Trigger para historico_conversa (embora seja mais append-only)
        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS trigger_historico_update
        AFTER UPDATE ON historico_conversa
        FOR EACH ROW
        BEGIN
            UPDATE historico_conversa 
            SET data_alteracao = CURRENT_TIMESTAMP 
            WHERE id_historico = OLD.id_historico;
        END;
        """)
        self.conn.commit()

    def obter_ou_criar_sessao(self, id_usuario: str, user_data: dict = None):
        """ 
        Busca uma sessão. Se não existir, cria uma nova.
        Sempre atualiza os dados do usuário se fornecidos.
        Retorna a linha completa da sessão como um dicionário.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sessoes_usuarios WHERE id_usuario = ?", (id_usuario,))
        sessao = cursor.fetchone()
        
        estado_padrao_json = json.dumps(_estado_padrao())

        if not sessao:
            # Sessão não existe, criar
            user_data = user_data or {}
            dados_insert = {
                "id_usuario": id_usuario,
                "first_name": user_data.get("first_name"),
                "last_name": user_data.get("last_name"),
                "username": user_data.get("username"),
                "estado": estado_padrao_json,
                "status_sessao": "MENU" # Nova sessão sempre começa no MENU
            }
            cursor.execute("""
            INSERT INTO sessoes_usuarios (id_usuario, first_name, last_name, username, estado, status_sessao)
            VALUES (:id_usuario, :first_name, :last_name, :username, :estado, :status_sessao)
            """, dados_insert)
            self.conn.commit()
            
            # Buscar o registro recém-criado para retornar
            cursor.execute("SELECT * FROM sessoes_usuarios WHERE id_usuario = ?", (id_usuario,))
            sessao = cursor.fetchone()
        
        elif user_data:
            # Sessão existe, atualizar dados do usuário se mudaram
            if (sessao.get('first_name') != user_data.get('first_name') or
                sessao.get('last_name') != user_data.get('last_name') or
                sessao.get('username') != user_data.get('username')):
                
                cursor.execute("""
                UPDATE sessoes_usuarios
                SET first_name = ?, last_name = ?, username = ?
                WHERE id_usuario = ?
                """, (user_data.get("first_name"), user_data.get("last_name"), 
                      user_data.get("username"), id_usuario))
                self.conn.commit()
                
                # Recarrega a sessão com dados atualizados
                sessao.update(user_data)

        return sessao # Retorna o dict da linha da sessão

    def salvar_estado_json(self, id_usuario: str, estado_json: str):
        """ Atualiza apenas o JSON de estado de uma sessão. """
        cursor = self.conn.cursor()
        cursor.execute("""
        UPDATE sessoes_usuarios SET estado = ? WHERE id_usuario = ?
        """, (estado_json, id_usuario))
        self.conn.commit()

    def mudar_status_sessao(self, id_usuario: str, novo_status: str):
        """ Atualiza apenas o status da sessão (ex: 'MENU', 'ATIVO'). """
        cursor = self.conn.cursor()
        cursor.execute("""
        UPDATE sessoes_usuarios SET status_sessao = ? WHERE id_usuario = ?
        """, (novo_status, id_usuario))
        self.conn.commit()

    def reiniciar_sessao_completa(self, id_usuario: str):
        """ Reseta o estado para o padrão e define o status como 'MENU'. """
        estado_padrao_json = json.dumps(_estado_padrao())
        cursor = self.conn.cursor()
        cursor.execute("""
        UPDATE sessoes_usuarios SET estado = ?, status_sessao = 'MENU' 
        WHERE id_usuario = ?
        """, (estado_padrao_json, id_usuario))
        self.conn.commit()
        return _estado_padrao() # Retorna o dict do estado padrão

    def log_historico(self, id_usuario: str, direcao: str, mensagem: str):
        """ Registra uma mensagem no histórico de conversa. """
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO historico_conversa (id_usuario, direcao, mensagem)
        VALUES (?, ?, ?)
        """, (id_usuario, direcao, mensagem))
        self.conn.commit()
