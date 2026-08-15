import os
import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

mensagem = """
🤖 Bot Caçador de Ofertas

✅ Conexão com o GitHub funcionando!

O bot está pronto para começar a pesquisar preços.
"""

resposta = requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": mensagem
    },
    timeout=30
)

resposta.raise_for_status()

print("Mensagem enviada com sucesso!")