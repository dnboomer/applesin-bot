import os
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler, 
                          MessageHandler, ConversationHandler, filters)

SELECTING_SERVICE, WAITING_FOR_PHONE = range(2)

PRICES = {
    "15pro_15promax": {"title": "15 Pro и 15 Pro Max", "services": [{"name": "акб стандарт:", "price": "4300"}, {"name": "акб фокскон:", "price": "5600"}]},
    "15_15plus": {"title": "iPhone 15 и 15 Plus", "services": [{"name": "акб стандарт:", "price": "4200"}, {"name": "акб фокскон:", "price": "5500"}]}
}

async def start(update, context):
    text = "Привет! Эплсин на связи. Что нужно?"
    kb = [[InlineKeyboardButton("Выбрать устройство", callback_data="devicelist")]]
    if update.callback_query: await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    else: await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))
    return SELECTING_SERVICE

async def device_list(update, context):
    await update.callback_query.edit_message_text("Выберите устройство:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("iPhone", callback_data="modellist")], [InlineKeyboardButton("Назад", callback_data="start")]]))
    return SELECTING_SERVICE

async def model_list(update, context):
    kb = [[InlineKeyboardButton("15 Pro/Max", callback_data="model_15pro_15promax"), InlineKeyboardButton("15/Plus", callback_data="model_15_15plus")],
          [InlineKeyboardButton("Назад", callback_data="devicelist")]]
    await update.callback_query.edit_message_text("Какая модель?", reply_markup=InlineKeyboardMarkup(kb))
    return SELECTING_SERVICE

async def show_price(update, context):
    query = update.callback_query
    model_key = query.data.replace("model_", "")
    context.user_data['model_key'] = model_key
    data = PRICES.get(model_key)
    kb = [[InlineKeyboardButton(f"{s['name']} {s['price']}₽", callback_data=f"service_{s['name']}")] for s in data['services']]
    kb.append([InlineKeyboardButton("Назад", callback_data="modellist")])
    await query.edit_message_text(f"Вы выбрали {data['title']}. Что нужно?", reply_markup=InlineKeyboardMarkup(kb))
    return SELECTING_SERVICE

async def book_menu(update, context):
    query = update.callback_query
    service_name = query.data.replace("service_", "")
    context.user_data['service'] = service_name
    model_key = context.user_data.get('model_key')
    path = f"iPhone — {PRICES[model_key]['title']} — {service_name}"
    context.user_data['path'] = path
    kb = [[InlineKeyboardButton("Поделиться контактом", request_contact=True)],
          [InlineKeyboardButton("Ввести вручную", callback_data="manual")],
          [InlineKeyboardButton("Назад", callback_data=f"model_{model_key}")]]
    await query.edit_message_text(f"Вы выбрали: {path}\n\nКак с вами связаться?", reply_markup=InlineKeyboardMarkup(kb))
    return WAITING_FOR_PHONE

async def receive_phone(update, context):
    if update.callback_query and update.callback_query.data == "manual":
        await update.callback_query.edit_message_text("Введите номер цифрами:")
        return WAITING_FOR_PHONE
    phone = update.message.contact.phone_number if update.message.contact else re.sub(r'\D', '', update.message.text)
    if not update.message.contact and not (10 <= len(phone) <= 11):
        await update.message.reply_text("Ошибка! Введите корректный номер.")
        return WAITING_FOR_PHONE
    if not update.message.contact: phone = f"+7 ({phone[-10:-7]}) {phone[-7:-4]}-{phone[-4:-2]}-{phone[-2:]}"
    await update.message.reply_text(f"Спасибо! Заявка:\n{context.user_data['path']}\nНомер: {phone}")
    return ConversationHandler.END

# Создаем список общих команд для навигации, которые работают ВСЕГДА
nav_handlers = [
    CallbackQueryHandler(start, pattern="^start$"),
    CallbackQueryHandler(device_list, pattern="^devicelist$"),
    CallbackQueryHandler(model_list, pattern="^modellist$"),
    CallbackQueryHandler(show_price, pattern="^model_")
]

app = Application.builder().token(os.environ["TOKEN"]).build()
app.add_handler(ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        SELECTING_SERVICE: nav_handlers + [CallbackQueryHandler(book_menu, pattern="^service_")],
        WAITING_FOR_PHONE: nav_handlers + [CallbackQueryHandler(book_menu, pattern="manual"), MessageHandler(filters.CONTACT | filters.TEXT & ~filters.COMMAND, receive_phone)]
    },
    fallbacks=[CommandHandler("start", start)]
))
app.run_polling()