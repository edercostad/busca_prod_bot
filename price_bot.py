import os
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# ==========================================
# FUNÇÕES DE PESQUISA DE PREÇOS
# ==========================================

def pesquisar_mercado_livre(produto: str, limite: int = 5):
    """Pesquisa preços no Mercado Livre"""
    resultados = []
    try:
        url = f"https://lista.mercadolivre.com.br/{produto.replace(' ', '-')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        items = soup.find_all('li', class_='ui-search-layout__item')[:limite]
        
        for item in items:
            try:
                titulo = item.find('h2', class_='ui-search-item__title').text.strip()
                preco = item.find('span', class_='andes-money-amount__fraction').text.strip()
                link = item.find('a', class_='ui-search-link')['href']
                
                # Limpar preço
                preco = preco.replace('.', '').replace(',', '.')
                preco_float = float(preco)
                
                resultados.append({
                    'loja': 'Mercado Livre',
                    'titulo': titulo,
                    'preco': preco_float,
                    'link': link
                })
            except:
                continue
    except Exception as e:
        print(f"Erro na pesquisa do Mercado Livre: {e}")
    
    return resultados


def pesquisar_precos(produto: str):
    """Agrega resultados de múltiplas lojas"""
    todos_resultados = []
    
    # Pesquisar no Mercado Livre
    ml = pesquisar_mercado_livre(produto)
    todos_resultados.extend(ml)
    
    # Adicione outras lojas aqui (Amazon, Magazine Luiza, etc.)
    
    # Ordenar por preço
    todos_resultados.sort(key=lambda x: x['preco'])
    
    return todos_resultados


# ==========================================
# COMANDOS DO BOT
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    mensagem = """
Olá! Eu sou o seu assistente de pesquisa de preços! 🛒

📌 **Como usar:**
- Envie o nome de qualquer produto que eu pesquisarei os melhores preços para você!

🔧 **Comandos disponíveis:**
`/pesquisar [produto]` - Pesquisa preços de um produto
`/ajuda` - Mostra esta mensagem de ajuda

💡 **Exemplo:**
Envie: `fone de ouvido bluetooth`
Ou use: `/pesquisar fone de ouvido bluetooth`
    """
    await update.message.reply_text(mensagem, parse_mode='Markdown')


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /ajuda"""
    await start(update, context)


async def pesquisar_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /pesquisar produto"""
    if not context.args:
        await update.message.reply_text("❌ Por favor, informe o produto!\nEx: `/pesquisar celular samsung`", parse_mode='Markdown')
        return
    
    produto = ' '.join(context.args)
    await realizar_pesquisa(update, produto)


async def mensagem_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde a qualquer mensagem de texto com pesquisa"""
    produto = update.message.text.strip()
    
    # Ignorar comandos
    if produto.startswith('/'):
        return
    
    await realizar_pesquisa(update, produto)


async def realizar_pesquisa(update: Update, produto: str):
    """Executa a pesquisa e envia resultados"""
    msg_espera = await update.message.reply_text(f"🔍 Pesquisando preços de **{produto}**...\nAguarde um momento!", parse_mode='Markdown')
    
    resultados = pesquisar_precos(produto)
    
    await msg_espera.delete()
    
    if not resultados:
        await update.message.reply_text(f"❌ Não encontrei resultados para **{produto}**.\nTente usar termos mais específicos.", parse_mode='Markdown')
        return
    
    # Montar mensagem de resposta
    resposta = f"✅ Encontrei {len(resultados)} resultados para **{produto}**:\n\n"
    
    for i, r in enumerate(resultados, 1):
        resposta += f"🏪 {r['loja']}\n"
        resposta += f"📦 {r['titulo'][:80]}...\n"
        resposta += f"💰 R$ {r['preco']:.2f}\n"
        resposta += f"🔗 [Ver produto]({r['link']})\n\n"
    
    # Melhor preço
    melhor = resultados[0]
    resposta += f"🏆 **Melhor preço:** R$ {melhor['preco']:.2f} na {melhor['loja']}"
    
    await update.message.reply_text(resposta, parse_mode='Markdown', disable_web_page_preview=True)


# ==========================================
# FUNÇÃO PARA EXECUÇÃO AUTOMÁTICA
# ==========================================

async def alerta_preco(produto: str, preco_maximo: float, chat_id: str):
    """Verifica preços e envia alerta se estiver abaixo do valor definido"""
    resultados = pesquisar_precos(produto)
    
    if not resultados:
        return
    
    melhor = resultados[0]
    
    if melhor['preco'] <= preco_maximo:
        mensagem = f"""
🚨 **ALERTA DE PREÇO BAIXO!** 🚨

📦 Produto: {produto}
💰 Preço encontrado: R$ {melhor['preco']:.2f}
🎯 Preço alvo: R$ {preco_maximo:.2f}
🏪 Loja: {melhor['loja']}
🔗 Link: {melhor['link']}
        """
        
        # Enviar mensagem diretamente
        from telegram import Bot
        bot = Bot(token=TOKEN)
        await bot.send_message(chat_id=chat_id, text=mensagem, parse_mode='Markdown')


# ==========================================
# INICIALIZAÇÃO DO BOT
# ==========================================

def main():
    print("🤖 Bot de Preços iniciado...")
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('ajuda', ajuda))
    application.add_handler(CommandHandler('pesquisar', pesquisar_comando))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem_texto))
    
    # Iniciar bot
    application.run_polling()


if __name__ == '__main__':
    main()
