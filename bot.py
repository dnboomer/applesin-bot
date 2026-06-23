import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

TOKEN = os.getenv('TOKEN')
ADMIN_ID = "867640"

MODELS = {
    'ip15': ['15 Pro / Pro Max', '15 / 15 Plus'],
    'ip14': ['14 Pro / Pro Max', '14 / 14 Plus'],
    'ip13': ['13 Pro / Pro Max', '13 mini / 13'],
    'ip12': ['12 Pro / Pro Max', '12 mini / 12'],
    'ip11': ['11 Pro / Pro Max', '11 / Xr / X / Xs / Xs Max'],
    'ipse': ['SE 2020 / SE 2022']
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(f"iPhone {k.replace('ip', '')}", callback_data=k)] for k in MODELS.keys()]
    await update.message.reply_text("Эплсин. Выберите серию:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data in MODELS:
        keyboard = [[InlineKeyboardButton(model, callback_data=f'order_{model}')] for model in MODELS[query.data]]
        keyboard.append([InlineKeyboardButton("« Назад", callback_data='back_start')])
        await query.edit_message_text("Выберите конкретную модель:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == 'back_start':
        keyboard = [[InlineKeyboardButton(f"iPhone {k.replace('ip', '')}", callback_data=k)] for k in MODELS.keys()]
        await query.edit_message_text("Эплсин. Выберите серию:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data.startswith('order_'):
        model = query.data.replace('order_', '')
        await query.edit_message_text(f"Принято ({model}). Введите ваш номер телефона:")

async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if any(c.isdigit() for c in text) and len(text) > 7:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"Новая заявка: {text}")
        await update.message.reply_text("Спасибо, мастер свяжется с вами.")
    else:
        await update.message.reply_text("Я вас не понял. Нажмите /start")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_phone))
    application.run_polling()
