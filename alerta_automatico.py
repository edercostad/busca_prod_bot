import asyncio
import os
from price_bot import alerta_preco
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# CONFIGURE AQUI OS PRODUTOS PARA MONITORAR
# ==========================================

PRODUTOS_MONITORADOS = [
    {"produto": "playstation 5", "preco_maximo": 3500.00},
    {"produto": "nintendo switch oled", "preco_maximo": 2000.00},
    # Adicione mais produtos aqui
]

CHAT_ID = os.getenv('CHAT_ID', '')  # Seu ID do Telegram

async def main():
    if not CHAT_ID:
        print("❌ Configure o CHAT_ID no arquivo .env")
        return
    
    print("🔍 Verificando preços...")
    
    for item in PRODUTOS_MONITORADOS:
        await alerta_preco(item['produto'], item['preco_maximo'], CHAT_ID)
    
    print("✅ Verificação concluída!")


if __name__ == '__main__':
    asyncio.run(main())
