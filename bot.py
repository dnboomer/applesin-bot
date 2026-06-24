import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

PRICES = {
    "15pro_15promax": [{"name": "АКБ", "price": "4300"}, {"name": "Дисплей", "price": "7000"}, {"name": "Шлейф", "price": "8500"}, {"name": "Камера", "price": "9500"}, {"name": "Face ID", "price": "9000"}, {"name": "Стекло", "price": "6000"}],
    "15_15plus": [{"name": "АКБ", "price": "4200"}, {"name": "Дисплей", "price": "5000"}, {"name": "Шлейф", "price": "8000"}, {"name": "Камера", "price": "9000"}, {"name": "Face ID", "price": "8000"}, {"name": "Стекло", "price": "5500"}],
    "14pro_14promax": [{"name": "АКБ", "price": "4300"}, {"name": "Дисплей", "price": "7000"}, {"name": "Шлейф", "price": "8500"}, {"name": "Камера", "price": "9500"}, {"name": "Face ID", "price": "9000"}, {"name": "Стекло", "price": "6000"}],
    "14_14plus": [{"name": "АКБ", "price": "4200"}, {"name": "Дисплей", "price": "5000"}, {"name": "Шлейф", "price": "8000"}, {"name": "Камера", "price": "9000"}, {"name": "Face ID", "price": "8000"}, {"name": "Стекло", "price": "5500"}],
    "13pro_13promax": [{"name": "АКБ", "price": "4300"}, {"name": "Дисплей", "price": "6000"}, {"name": "Шлейф", "price": "8500"}, {"name": "Камера", "price": "9000"}, {"name": "Face ID", "price": "8500"}, {"name": "Стекло", "price": "6000"}],
    "13mini_13": [{"name": "АКБ", "price": "4100"}, {"name": "Дисплей", "price": "5000"}, {"name": "Шлейф", "price": "6500"}, {"name": "Камера", "price": "8000"}, {"name": "Face ID", "price": "8000"}, {"name": "Стекло", "price": "5500"}],
    "12pro_12promax": [{"name": "АКБ", "price": "4300"}, {"name": "Дисплей", "price": "6000"}, {"name": "Шлейф", "price": "8500"}, {"name": "Камера", "price": "9000"}, {"name": "Face ID", "price": "8500"}, {"name": "Стекло", "price": "6000"}],
    "12mini_12": [{"name": "АКБ", "price": "4100"}, {"name": "Дисплей", "price": "5000"}, {"name": "Шлейф", "price": "6500"}, {"name": "Камера", "price": "8000"}, {"name": "Face ID", "price": "8000"}, {"name": "Стекло", "price": "5500"}],
    "11pro_11promax": [{"name": "АКБ", "price": "3200"}, {"name": "Дисплей", "price": "3000"}, {"name": "Шлейф", "price": "2900"}, {"name": "Камера", "price": "5000"}, {"name": "Face ID", "price": "5000"}, {"name": "Стекло", "price": "4500"}],
    "xr_11": [{"name": "АКБ", "price": "3000"}, {"name": "Дисплей", "price": "2800"}, {"name": "Шлейф", "price": "3000"}, {"name": "Камера", "price": "4500"}, {"name": "Face ID", "price": "4000"}, {"name": "Стекло", "price": "4000"}],
    "x_xs_xsmax": [{"name": "АКБ", "price": "2500"}, {"name": "Дисплей", "price": "2500"}, {"name": "Шлейф", "price": "3000"}, {"name": "Камера", "price": "4500"}, {"name": "Face ID", "price": "3500"}, {"name": "Стекло", "price": "3500"}],
    "se2020_se2022": [{"name": "Уточняйте у мастера", "price": "0"}]
}

async def start(update, context):
    text = "Привет! Эплсин на связи. Что нужно?"
    kb = [[InlineKeyboardButton("Выбрать устройство", callback_data="devicelist")]]
    if update.callback_query: await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    else: await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))

async def device_list(update, context):
    await update.callback_query.edit_message_text("Выбери устройство:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("iPhone", callback_data="modellist")], [InlineKeyboardButton("Назад", callback_data="start")]]))

async def model_list(update, context):
    keyboard = [
        [InlineKeyboardButton("15 Pro и 15 Pro Max", callback_data="model_15pro_15promax"), InlineKeyboardButton("15 и 15 Plus", callback_data="model_15_15plus")],
        [InlineKeyboardButton("14 Pro и 14 Pro Max", callback_data="model_14pro_14promax"), InlineKeyboardButton("14 и 14 Plus", callback_data="model_14_14plus")],
        [InlineKeyboardButton("13 Pro и 13 Pro Max", callback_data="model_13pro_13promax"), InlineKeyboardButton("13 mini и 13", callback_data="model_13mini_13")],
        [InlineKeyboardButton("12 Pro и 12 Pro Max", callback_data="model_12pro_12promax"), InlineKeyboardButton("12 mini и 12", callback_data="model_12mini_12")],
        [InlineKeyboardButton("11 Pro и 11 Pro Max", callback_data="model_11pro_11promax"), InlineKeyboardButton("Xr и 11", callback_data="model_xr_11")],
        [InlineKeyboardButton("X, Xs и Xs Max", callback_data="model_x_xs_xsmax"), InlineKeyboardButton("SE 2020 и SE 2022", callback_data="model_se2020_se2022")],
        [InlineKeyboardButton("Назад", callback_data="devicelist")]
    ]
    await update.callback_query.edit_message_text("Выберите модель:", reply_markup=InlineKeyboardMarkup(keyboard))

async def show_price(update, context):
    query = update.callback_query
    model_key = query.data.replace("model_", "")
    services = PRICES.get(model_key, [])
    keyboard = [[InlineKeyboardButton(f"{s['name']} - {s['price']}", callback_data="book_service")] for s in services]
    keyboard.append([InlineKeyboardButton("Назад", callback_data="modellist")])
    await query.edit_message_text("Выберите услугу:", reply_markup=InlineKeyboardMarkup(keyboard))

async def book_menu(update, context):
    kb = [[InlineKeyboardButton("Поделиться контактом", callback_data="share_contact")], [InlineKeyboardButton("Ввести вручную", callback_data="manual_number")], [InlineKeyboardButton("Назад", callback_data="modellist")]]
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