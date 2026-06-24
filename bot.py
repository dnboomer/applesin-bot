import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

PRICES = {
    "15pro_15promax": "15 Pro и 15 Pro Max:\nАккумулятор: 4300-5600\nДисплей: 7000-35000\nНижний шлейф: 8500\nКамера: 9500\nFace ID: 9000\nЗаднее стекло: 6000",
    "15_15plus": "15 и 15 Plus:\nАккумулятор: 4200-5500\nДисплей: 5000-30000\nНижний шлейф: 8000\nКамера: 9000\nFace ID: 8000\nЗаднее стекло: 5500",
    "14pro_14promax": "14 Pro и 14 Pro Max:\nАккумулятор: 4300-5600\nДисплей: 7000-35000\nНижний шлейф: 8500\nКамера: 9500\nFace ID: 9000\nЗаднее стекло: 6000",
    "14_14plus": "14 и 14 Plus:\nАккумулятор: 4200-5500\nДисплей: 5000-30000\nНижний шлейф: 8000\nКамера: 9000\nFace ID: 8000\nЗаднее стекло: 5500",
    "13pro_13promax": "13 Pro и 13 Pro Max:\nАккумулятор: 4300-5600\nДисплей: 6000-34000\nНижний шлейф: 8500\nКамера: 9000\nFace ID: 8500\nЗаднее стекло: 6000",
    "13mini_13": "13 mini и 13:\nАккумулятор: 4100-5500\nДисплей: 5000-13000\nНижний шлейф: 6500\nКамера: 8000\nFace ID: 8000\nЗаднее стекло: 5500",
    "12pro_12promax": "12 Pro и 12 Pro Max:\nАккумулятор: 4300-5600\nДисплей: 6000-34000\nНижний шлейф: 8500\nКамера: 9000\nFace ID: 8500\nЗаднее стекло: 6000",
    "12mini_12": "12 mini и 12:\nАккумулятор: 4100-5500\nДисплей: 5000-13000\nНижний шлейф: 6500\nКамера: 8000\nFace ID: 8000\nЗаднее стекло: 5500",
    "11pro_11promax": "11 Pro и 11 Pro Max:\nАккумулятор: 3200-4500\nДисплей: 3000-9000\nНижний шлейф: 2900\nКамера: 5000\nFace ID: 5000\nЗаднее стекло: 4500",
    "xr_11": "Xr и 11:\nАккумулятор: 3000-4200\nДисплей: 2800-4900\nНижний шлейф: 3000\nКамера: 4500\nFace ID: 4000\nЗаднее стекло: 4000",
    "x_xs_xsmax": "X, Xs и Xs Max:\nАккумулятор: 2500-3200\nДисплей: 2500-3500\nНижний шлейф: 3000\nКамера: 4500\nFace ID: 3500\nЗаднее стекло: 3500",
    "se2020_se2022": "SE 2020 и SE 2022:\nЦены уточняйте у мастера"
}

async def start(update, context):
    keyboard = [[InlineKeyboardButton("Выбрать устройство", callback_data="devicelist")], [InlineKeyboardButton("Выбрать проблему", callback_data="select_problem")]]
    await update.message.reply_text("Привет! Эплсин на связи. Что нужно?", reply_markup=InlineKeyboardMarkup(keyboard))

async def device_list(update, context):
    keyboard = [[InlineKeyboardButton("iPhone", callback_data="device_iphone")], [InlineKeyboardButton("Назад", callback_data="start")]]
    await update.callback_query.edit_message_text("Выбери устройство:", reply_markup=InlineKeyboardMarkup(keyboard))

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
    text = PRICES.get(model_key, "Прайс уточняется.")
    keyboard = [[InlineKeyboardButton("Замена АКБ", callback_data="book_akb")], [InlineKeyboardButton("Нет моей проблемы", callback_data="contact_master")], [InlineKeyboardButton("Назад", callback_data="modellist")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def book_menu(update, context):
    keyboard = [[InlineKeyboardButton("Поделиться контактом", callback_data="share_contact")], [InlineKeyboardButton("Ввести вручную", callback_data="manual_number")], [InlineKeyboardButton("Написать мастеру", callback_data="contact_master")], [InlineKeyboardButton("Назад", callback_data="price")]]
    await update.callback_query.edit_message_text("Как с вами связаться?", reply_markup=InlineKeyboardMarkup(keyboard))

app = Application.builder().token(os.environ["TOKEN"]).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(device_list, pattern="devicelist"))
app.add_handler(CallbackQueryHandler(model_list, pattern="device_iphone"))
app.add_handler(CallbackQueryHandler(show_price, pattern="model_"))
app.add_handler(CallbackQueryHandler(book_menu, pattern="book_"))
app.run_polling()