import os, re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters
from data import PRICES

async def start(update, context):
    context.user_data.clear()
    kb = [[InlineKeyboardButton("Выбрать устройство", callback_data="model_list")]]
    await update.message.reply_text("Привет! Эплсин на связи. Что нужно?", reply_markup=InlineKeyboardMarkup(kb))

async def model_list(update, context):
    query = update.callback_query
    await query.answer()
    kb = [[InlineKeyboardButton(data['title'], callback_data=f"select_{m}")] for m, data in PRICES.items()]
    await query.edit_message_text("Какая модель?", reply_markup=InlineKeyboardMarkup(kb))

async def service_list(update, context):
    query = update.callback_query
    await query.answer()
    model = query.data.split("_")[1]
    context.user_data['model'] = model
    kb = [[InlineKeyboardButton(f"{s['name']} {s['price']}₽", callback_data=f"book_{s['name']}")] for s in PRICES[model]['services']]
    kb.append([InlineKeyboardButton("Назад", callback_data="model_list")])
    await query.edit_message_text(f"Вы выбрали {PRICES[model]['title']}. Что нужно?", reply_markup=InlineKeyboardMarkup(kb))

async def get_contact(update, context):
    query = update.callback_query
    await query.answer()
    service = query.data.split("_")[1]
    context.user_data['service'] = service
    path = f"iPhone — {PRICES[context.user_data['model']]['title']} — {service}"
    context.user_data['path'] = path
    await query.edit_message_text(f"Вы выбрали: {path}\n\nВведите номер телефона:")

async def final_handler(update, context):
    phone = re.sub(r'\D', '', update.message.text)
    if 10 <= len(phone) <= 11:
        clean_phone = f"+7 ({phone[-10:-7]}) {phone[-7:-4]}-{phone[-4:-2]}-{phone[-2:]}"
        await update.message.reply_text(f"Спасибо! Заявка принята.\nПуть: {context.user_data['path']}\nНомер: {clean_phone}")
    else:
        await update.message.reply_text("Ошибка! Введите корректный номер.")

app = Application.builder().token(os.environ["TOKEN"]).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(model_list, pattern="model_list"))
app.add_handler(CallbackQueryHandler(service_list, pattern="select_"))
app.add_handler(CallbackQueryHandler(get_contact, pattern="book_"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, final_handler))
app.run_polling()
