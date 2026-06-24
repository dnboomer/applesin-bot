import os
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler, 
                          MessageHandler, ConversationHandler, filters)

SELECTING_SERVICE, WAITING_FOR_PHONE = range(2)

PRICES = {
    "15pro_15promax": {"title": "15 Pro и 15 Pro Max", "services": [{"name": "акб стандарт:", "price": "4300"}, {"name": "акб фокскон:", "price": "5600"}, {"name": "диспл дешев:", "price": "7000-8000"}, {"name": "диспл средн:", "price": "12000-15000"}, {"name": "диспл дорог:", "price": "20000-35000"}, {"name": "нижний шлейф:", "price": "8500"}, {"name": "камера:", "price": "9500"}, {"name": "фэйсайди:", "price": "9000"}, {"name": "заднее стекло:", "price": "6000"}]},
    "15_15plus": {"title": "iPhone 15 и 15 Plus", "services": [{"name": "акб стандарт:", "price": "4200"}, {"name": "акб фокскон:", "price": "5500"}, {"name": "диспл дешев:", "price": "5000-7000"}, {"name": "диспл средн:", "price": "10000-12000"}, {"name": "диспл дорог:", "price": "15000-18000"}, {"name": "нижний шлейф:", "price": "8000"}, {"name": "камера:", "price": "9000"}, {"name": "фэйсайди:", "price": "8000"}, {"name": "заднее стекло:", "price": "5500"}]},
    "14pro_14promax": {"title": "14 Pro и 14 Pro Max", "services": [{"name": "акб стандарт:", "price": "4300"}, {"name": "акб фокскон:", "price": "5600"}, {"name": "диспл дешев:", "price": "7000-8000"}, {"name": "диспл средн:", "price": "12000-15000"}, {"name": "диспл дорог:", "price": "20000-35000"}, {"name": "нижний шлейф:", "price": "8500"}, {"name": "камера:", "price": "9500"}, {"name": "фэйсайди:", "price": "9000"}, {"name": "заднее стекло:", "price": "6000"}]},
    "14_14plus": {"title": "iPhone 14 и 14 Plus", "services": [{"name": "акб стандарт:", "price": "4200"}, {"name": "акб фокскон:", "price": "5500"}, {"name": "диспл дешев:", "price": "5000-7000"}, {"name": "диспл средн:", "price": "10000-12000"}, {"name": "диспл дорог:", "price": "15000-18000"}, {"name": "нижний шлейф:", "price": "8000"}, {"name": "камера:", "price": "9000"}, {"name": "фэйсайди:", "price": "8000"}, {"name": "заднее стекло:", "price": "5500"}]},
    "13pro_13promax": {"title": "13 Pro и 13 Pro Max", "services": [{"name": "акб стандарт:", "price": "4300"}, {"name": "акб фокскон:", "price": "5600"}, {"name": "диспл дешев:", "price": "6000-8000"}, {"name": "диспл средн:", "price": "10000-15000"}, {"name": "диспл дорог:", "price": "18000-34000"}, {"name": "нижний шлейф:", "price": "8500"}, {"name": "камера:", "price": "9000"}, {"name": "фэйсайди:", "price": "8500"}, {"name": "заднее стекло:", "price": "6000"}]},
    "13mini_13": {"title": "iPhone 13 mini и 13", "services": [{"name": "акб стандарт:", "price": "4100"}, {"name": "акб фокскон:", "price": "5500"}, {"name": "диспл дешев:", "price": "5000-6000"}, {"name": "диспл средн:", "price": "7000-9000"}, {"name": "диспл дорог:", "price": "10000-13000"}, {"name": "нижний шлейф:", "price": "6500"}, {"name": "камера:", "price": "8000"}, {"name": "фэйсайди:", "price": "8000"}, {"name": "заднее стекло:", "price": "5500"}]},
    "12pro_12promax": {"title": "12 Pro и 12 Pro Max", "services": [{"name": "акб стандарт:", "price": "4300"}, {"name": "акб фокскон:", "price": "5600"}, {"name": "диспл дешев:", "price": "6000-8000"}, {"name": "диспл средн:", "price": "10000-15000"}, {"name": "диспл дорог:", "price": "18000-34000"}, {"name": "нижний шлейф:", "price": "8500"}, {"name": "камера:", "price": "9000"}, {"name": "фэйсайди:", "price": "8500"}, {"name": "заднее стекло:", "price": "6000"}]},
    "12mini_12": {"title": "12 mini и 12", "services": [{"name": "акб стандарт:", "price": "4100"}, {"name": "акб фокскон:", "price": "5500"}, {"name": "диспл дешев:", "price": "5000-6000"}, {"name": "диспл средн:", "price": "7000-9000"}, {"name": "диспл дорог:", "price": "10000-13000"}, {"name": "нижний шлейф:", "price": "6500"}, {"name": "камера:", "price": "8000"}, {"name": "фэйсайди:", "price": "8000"}, {"name": "заднее стекло:", "price": "5500"}]},
    "11pro_11promax": {"title": "11 Pro и 11 Pro Max", "services": [{"name": "акб стандарт:", "price": "3200"}, {"name": "акб фокскон:", "price": "4500"}, {"name": "диспл дешев:", "price": "3000-4000"}, {"name": "диспл средн:", "price": "5000-6000"}, {"name": "диспл дорог:", "price": "7000-9000"}, {"name": "нижний шлейф:", "price": "2900"}, {"name": "камера:", "price": "5000"}, {"name": "фэйсайди:", "price": "5000"}, {"name": "заднее стекло:", "price": "4500"}]},
    "xr_11": {"title": "iPhone Xr и 11", "services": [{"name": "акб стандарт:", "price": "3000"}, {"name": "акб фокскон:", "price": "4200"}, {"name": "диспл дешев:", "price": "2800-3000"}, {"name": "диспл средн:", "price": "3500-4000"}, {"name": "диспл дорог:", "price": "4500-4900"}, {"name": "нижний шлейф:", "price": "3000"}, {"name": "камера:", "price": "4500"}, {"name": "фэйсайди:", "price": "4000"}, {"name": "заднее стекло:", "price": "4000"}]},
    "x_xs_xsmax": {"title": "iPhone X, Xs и Xs Max", "services": [{"name": "акб стандарт:", "price": "2500"}, {"name": "акб фокскон:", "price": "3200"}, {"name": "диспл дешев:", "price": "2500-2800"}, {"name": "диспл средн:", "price": "3000-3200"}, {"name": "диспл дорог:", "price": "3500"}, {"name": "нижний шлейф:", "price": "3000"}, {"name": "камера:", "price": "4500"}, {"name": "фэйсайди:", "price": "3500"}, {"name": "заднее стекло:", "price": "3500"}]},
    "se2020_se2022": {"title": "iPhone SE 2020 и 2022", "services": [{"name": "уточняйте у мастера", "price": ""}]}
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
          [InlineKeyboardButton("14 Pro/Max", callback_data="model_14pro_14promax"), InlineKeyboardButton("14/Plus", callback_data="model_14_14plus")],
          [InlineKeyboardButton("13 Pro/Max", callback_data="model_13pro_13promax"), InlineKeyboardButton("13/Mini", callback_data="model_13mini_13")],
          [InlineKeyboardButton("12 Pro/Max", callback_data="model_12pro_12promax"), InlineKeyboardButton("12/Mini", callback_data="model_12mini_12")],
          [InlineKeyboardButton("11 Pro/Max", callback_data="model_11pro_11promax"), InlineKeyboardButton("Xr/11", callback_data="model_xr_11")],
          [InlineKeyboardButton("X/Xs/Max", callback_data="model_x_xs_xsmax"), InlineKeyboardButton("SE 2020/22", callback_data="model_se2020_se2022")],
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
        await update.message.reply_text("Ошибка! Введите корректный номер (10-11 цифр).")
        return WAITING_FOR_PHONE
    if not update.message.contact: phone = f"+7 ({phone[-10:-7]}) {phone[-7:-4]}-{phone[-4:-2]}-{phone[-2:]}"
    await update.message.reply_text(f"Спасибо! Заявка:\n{context.user_data['path']}\nНомер: {phone}")
    return ConversationHandler.END

app = Application.builder().token(os.environ["TOKEN"]).build()
app.add_handler(ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        SELECTING_SERVICE: [CallbackQueryHandler(start, pattern="^start$"), CallbackQueryHandler(device_list, pattern="^devicelist$"), CallbackQueryHandler(model_list, pattern="^modellist$"), CallbackQueryHandler(show_price, pattern="^model_"), CallbackQueryHandler(book_menu, pattern="^service_")],
        WAITING_FOR_PHONE: [CallbackQueryHandler(show_price, pattern="^model_"), CallbackQueryHandler(modellist_back, pattern="^modellist$"), CallbackQueryHandler(book_menu, pattern="manual"), MessageHandler(filters.CONTACT | filters.TEXT & ~filters.COMMAND, receive_phone)]
    },
    fallbacks=[CommandHandler("start", start)]
))
app.run_polling()