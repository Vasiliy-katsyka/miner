from flask import Flask, request, jsonify
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from googletrans import Translator

app = Flask(__name__)
bot = Bot(token='8148259500:AAEjvQpilZuAQ15N_3u7l_ggdbvdT-TEELo')  # Replace with your bot token
translator = Translator()

@app.route('/generate-invoice', methods=['POST'])
def generate_invoice():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    payload = data.get('payload')
    currency = data.get('currency')
    prices = data.get('prices')

    invoice_link = bot.create_invoice_link(
        title=title,
        description=description,
        payload=payload,
        provider_token='',  # Provider token must be empty for Telegram Stars
        currency=currency,
        prices=prices
    )

    return jsonify({'invoiceLink': invoice_link})

@bot.message_handler(commands=['start'])
def start(message):
    web_app = WebAppInfo(url='https://your-app-url.com') 
    button = InlineKeyboardButton(text='Start Mining', web_app=web_app)
    keyboard = InlineKeyboardMarkup([[button]])

    bot.send_message(
        chat_id=message.chat.id,
        text='Welcome to Pixel Miner! Start mining by clicking this button:',
        reply_markup=keyboard
    )

@app.route('/translate', methods=['GET'])
def translate_text():
    text = request.args.get('text')
    target_language = request.args.get('lang')
    translation = translator.translate(text, dest=target_language)
    return jsonify({'translated_text': translation.text})

if __name__ == '__main__':
    app.run(debug=True)
