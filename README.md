# busca_prod_bot
Bot para busca e monitoramento de preços 
# 🤖 Bot Telegram - Pesquisa de Preços Automática

Bot do Telegram que pesquisa preços de produtos automaticamente e envia alertas quando os preços baixam!

## ✨ Funcionalidades

- 🔍 Pesquisa preços em tempo real no Mercado Livre
- 📊 Ordena resultados do menor para o maior preço
- 🚨 Sistema de alerta automático quando preço cai
- ⏰ Execução automática a cada 6 horas via GitHub Actions
- 📱 Interface simples pelo Telegram

## 🚀 Como usar o bot

1. Abra seu bot no Telegram
2. Envie `/start` para ver as instruções
3. Envie o nome de qualquer produto para pesquisar
4. Ou use `/pesquisar nome-do-produto`

## ⚙️ Configuração

### 1. Variáveis de Ambiente (Secrets no GitHub)

Vá em **Settings > Secrets and variables > Actions > New repository secret** e adicione:

- `TELEGRAM_BOT_TOKEN`: Token do seu bot (obtido no @BotFather)
- `CHAT_ID`: Seu ID do Telegram (para receber alertas)

### 2. Como obter seu CHAT_ID

1. Envie uma mensagem para o bot
2. Acesse no navegador: `https://api.telegram.org/botSEU_TOKEN/getUpdates`
3. Procure por `"chat":{"id":123456789,...}` - esse número é seu CHAT_ID

### 3. Configurar produtos monitorados

Edite o arquivo `alerta_automatico.py` e adicione os produtos que deseja monitorar:

```python
PRODUTOS_MONITORADOS = [
    {"produto": "nome do produto", "preco_maximo": 100.00},
]
