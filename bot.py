import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

# Пример структуры для одной модели
PRICES = {
    "15pro_15promax": [
        {"name": "Замена аккумулятора (стандартный аналог)", "price": "4300"},
        {"name": "Замена аккумулятора (фоксконн)", "price": "5600"},
        {"name": "Замена дисплея", "price": "от 7000"}
    ]
}

async def start(update, context):
    query = update.callback_query
    text = "Привет! Эплсин на связи. Что нужно?"
    kb = [[InlineKeyboardButton("Выбрать устройство", callback_data="devicelist")]]
    if query: await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    else: await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))

async def device_list(update, context):
    await update.callback_query.edit_message_text("Выбери устройство:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("iPhone", callback_data="modellist")], [InlineKeyboardButton("Назад", callback_data="start")]]))

async def model_list(update, context):
    keyboard = [
        [InlineKeyboardButton("15 Pro и 15 Pro Max", callback_data="model_15pro_15promax")],
        [InlineKeyboardButton("Назад", callback_data="devicelist")]
    ]
    await update.callback_query.edit_message_text("Выберите модель:", reply_markup=InlineKeyboardMarkup(keyboard))

async def show_price(update, context):
    query = update.callback_query
    model_key = query.data.replace("model_", "")
    services = PRICES.get(model_key, [])
    keyboard = [[InlineKeyboardButton(f"{s['name']}\n{s['price']}", callback_data="book_service")] for s in services]
    keyboard.append([InlineKeyboardButton("Нет моей проблемы", callback_data="contact_master")])
    keyboard.append([InlineKeyboardButton("Назад", callback_data="modellist")])
    await query.edit_message_text("Выберите услугу:", reply_markup=InlineKeyboardMarkup(keyboard))

async def book_menu(update, context):
    kb = [[InlineKeyboardButton("Поделиться контактом", callback_data="share_contact")], [InlineKeyboardButton("Ввести вручную", callback_data="manual_number")], [InlineKeyboardButton("Написать мастеру", callback_data="contact_master")], [InlineKeyboardButton("Назад", callback_data="modellist")]]
    await update.callback_query.edit_message_text("Как с вами связаться?", reply_markup=InlineKeyboardMarkup(kb))

async def button_handler(update, context):
    query = update.callback_query
    await query.answer()
    if query.data == "start": await start(update, context)
    elif query.data == "devicelist": await device_list(update, context)
    elif query.data == "modellist": await model_list(update, context)
    elif query.data.startswith("model_"): await show_price(update, context)
    elif query.data == "book_service": await book_menu(update, context)

app = Application.builder().token(os.environ["TOKEN"]).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.run_polling()