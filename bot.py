import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

PRICES = {
    "xr_11": "Цены на ремонт iPhone Xr и 11:\nАккумулятор (стандарт): 3000\nАккумулятор (фоксконн): 4200\nДисплей (подешевле): 2800\nДисплей (получше): 3500\nДисплей (оригинал): 4900\nНижний шлейф: 3000\nКамера: 4500\nFace ID: 4000\nЗаднее стекло: 4000",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Выбрать устройство", callback_data="devicelist")], [InlineKeyboardButton("Выбрать проблему", callback_data="select_problem")]]
    await update.message.reply_text("Привет! Эплсин на связи. Что нужно?", reply_markup=InlineKeyboardMarkup(keyboard))

async def device_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("iPhone", callback_data="device_iphone")], [InlineKeyboardButton("Назад", callback_data="start")]]
    await update.callback_query.edit_message_text("Выбери устройство:", reply_markup=InlineKeyboardMarkup(keyboard))

async def model_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Xr и 11", callback_data="model_xr_11")], [InlineKeyboardButton("Назад", callback_data="devicelist")]]
    await update.callback_query.edit_message_text("Выбери модель:", reply_markup=InlineKeyboardMarkup(keyboard))

async def show_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    model_key = query.data.replace("model_", "")
    text = PRICES.get(model_key, "Прайс уточняется.")
    keyboard = [[InlineKeyboardButton("Замена АКБ", callback_data="book_akb")], [InlineKeyboardButton("Нет моей проблемы", callback_data="contact_master")], [InlineKeyboardButton("Назад", callback_data="modellist")]]
    await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def book_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Поделиться контактом", callback_data="share_contact")], [InlineKeyboardButton("Ввести вручную", callback_data="manual_number")], [InlineKeyboardButton("Написать мастеру", callback_data="contact_master")], [InlineKeyboardButton("Назад", callback_data="price")]]
    await update.callback_query.edit_message_text("Как с вами связаться?", reply_markup=InlineKeyboardMarkup(keyboard))

app = Application.builder().token(os.environ["TOKEN"]).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(device_list, pattern="devicelist"))
app.add_handler(CallbackQueryHandler(model_list, pattern="device_iphone"))
app.add_handler(CallbackQueryHandler(show_price, pattern="model_"))
app.add_handler(CallbackQueryHandler(book_menu, pattern="book_"))
app.run_polling()