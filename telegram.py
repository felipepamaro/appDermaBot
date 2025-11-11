import os
import httpx
from pydantic import BaseModel
from typing import Optional
import requests 


class Chat(BaseModel):
    id: int = 0
    first_name: Optional[str] = '' 
    last_name: Optional[str] = '' 
    username: Optional[str] = '' 
    type: Optional[str] = '' 

class Voice(BaseModel):
    duration: Optional[int] = 0
    mime_type: Optional[str] = '' 
    file_id: Optional[str] = '' 
    file_unique_id: Optional[str] = '' 
    file_size: Optional[int] = ''
    
class Message(BaseModel):
    message_id: int = 0
    chat: Optional[Chat] = None
    date: int = 0
    text: Optional[str] = '' 
    voice: Optional[Voice] = None

class TelegramMessage(BaseModel):
    message: Optional[Message]
    update_id: int =0

    

class TelegramSender:
    """
    Classe wrapper para enviar mensagens usando a API de Bot do Telegram.
    """
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.token:
            raise ValueError("A variável de ambiente TELEGRAM_BOT_TOKEN não está configurada!")
            
        self.api_url = f"https://api.telegram.org/bot{self.token}"
        self.client = httpx.Client()

    def send_message(self, chat_id: int, message: str):
        """
        Envia uma mensagem de texto para um chat_id específico do Telegram.
        
        Args:
            chat_id (int): O ID do chat do usuário.
            message (str): O conteúdo da mensagem a ser enviada.
        """
        if chat_id==123456789:
            print(f"Chat_id {chat_id} nenhuma mensagem será enviada'")
        else:
            endpoint = f"{self.api_url}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message
            }
            try:
                response = self.client.post(endpoint, json=payload)
                response.raise_for_status() #controla o erro caso a API falhe.
                print(f"Mensagem enviada para {chat_id}: '{message}'")
            except httpx.HTTPStatusError as e:
                print(f"Erro ao enviar mensagem para {chat_id}: {e.response.text}")
            except Exception as e:
                print(f"Erro ao enviar mensagem para {chat_id}: {e}")

    def __del__(self):
        # Garante que o cliente httpx seja fechado corretamente
        if hasattr(self, 'client'):
            self.client.close()
            
            
## TODO converter esta função para um metodo da classe principal. 
        
def Telegram_voicepath(file_id: str):

  TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/"
  TELEGRAM_FILE_URL = "https://api.telegram.org/file/bot{token}/{file_path}"

  TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
 

  base_url = TELEGRAM_API_URL.format(token=TELEGRAM_TOKEN)

  try:
    get_file_url = base_url + "getFile"
    response = requests.get(get_file_url, params={"file_id": file_id})
    response.raise_for_status() # Lança uma exceção para códigos de status HTTP 4xx/5xx

    file_info = response.json()
    file_path = file_info["result"]["file_path"]

    print(f"file_path obtido: {file_path}")

  except requests.exceptions.RequestException as e:
      print(f"Erro ao se comunicar com a API do Telegram (getFile): {e}")

  download_url = TELEGRAM_FILE_URL.format(token=TELEGRAM_TOKEN, file_path=file_path)

  return download_url