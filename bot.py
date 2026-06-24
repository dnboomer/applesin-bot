import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

PRICES = {
    "15pro_15promax": {"title": "15 Pro и 15 Pro Max", "services": [{"name": "акб стандарт:", "price": "4300"}, {"name": "акб фокскон:", "price": "5600"}, {"name": "диспл дешев:", "price": "7000-8000"}, {"name": "диспл средн:", "price": "12000-15000"}, {"name": "диспл дорог:", "price": "20000-35000"}, {"name": "нижний шлейф:", "price": "8500"}, {"name": "камера:", "price": "9500"}, {"name": "фэйсайди:", "price": "9000"}, {"name": "заднее стекло:", "price": "6000"}]},
    "15_15plus": {"title": "iPhone 15 и 15 Plus", "services": [{"name": "акб стандарт:", "price": "4200"}, {"name": "акб фокскон:", "price": "5500"}, {"name": "диспл дешев:", "price": "5000-7000"}, {"name": "диспл средн:", "price": "10000-12000"}, {"name": "диспл дорог:", "price": "15000-18000"}, {"name": "нижний шлейф:", "price": "8000"}, {"name": "камера:", "price": "9000"}, {"name": "фэйсайди:", "price": "8000"}, {"name": "заднее стекло:", "price": "5500"}]},
    "14pro_14promax": {"title": "14 Pro и 14 Pro Max", "services": [{"name": "акб стандарт:", "price": "4300"}, {"name": "акб фокскон:", "price": "5600"}, {"name": "диспл дешев:", "price": "7000-8000"}, {"name": "диспл средн:", "price": "12000-15000"}, {"name": "диспл дорог:", "price": "20000-35000"}, {"name": "нижний шлейф:", "price": "8500"}, {"name": "камера:", "price": "9500"}, {"name": "фэйсайди:", "price": "9000"}, {"name": "заднее стекло:", "price": "6000"}]},
    "14_14plus": {"title": "iPhone 14 и 14 Plus", "services": [{"name": "акб стандарт:", "price": "4200"}, {"name": "акб фокскон:", "price": "5500"}, {"name": "диспл дешев:", "price": "5000-7000"}, {"name": "диспл средн:", "price": "10000-12000"}, {"name": "диспл дорог:", "price": "15000-18000"}, {"name": "нижний шлейф:", "price": "8000"}, {"name": "камера:", "price": "9000"}, {"name": "фэйсайди:", "price": "8000"}, {"name": "заднее стекло:", "price": "5500"}]},
    "13pro_13promax": {"title": "13 Pro и 13 Pro Max", "services": [{"name": "акб стандарт:", "price": "4300"}, {"name": "акб фокскон:", "price": "5600"}, {"name": "диспл дешев:", "price": "6000-8000"}, {"name": "диспл средн:", "price": "10000-15000"}, {"name": "диспл дорог:", "price": "18000-34000"}, {"name": "нижний шлейф:", "price": "8500"}, {"name": "камера:", "price": "9000"}, {"name": "фэйсайди:", "price": "8500"}, {"name": "заднее стекло:", "price": "6000"}]},
    "13mini_13": {"title": "iPhone 13 mini и 13", "services": [{"name": "акб стандарт:", "price": "4100"}, {"name": "акб фокскон:", "price": "5500"}, {"name": "диспл дешев:", "price": "5000-6000"}, {"name": "диспл средн:", "price": "7000-9000"}, {"name": "диспл дорог:", "price": "10000-13000"}, {"name": "нижний шлейф:", "price": "6500"}, {"name": "камера:", "price": "8000"}, {"name": "фэйсайди:", "price": "8000"}, {"name": "заднее стекло:", "price": "5500"}]},
    "12pro_12promax": {"title": "12 Pro и 12 Pro Max", "services": [{"name": "акб стандарт:", "price": "4300"}, {"name": "акб фокскон:", "price": "5600"}, {"name": "диспл дешев:", "price": "6000-8000"}, {"name": "диспл средн:", "price": "10000-15000"}, {"name": "диспл дорог:", "price": "18000-34000"}, {"name": "нижний шлейф:", "price": "8500"}, {"name": "камера:", "price": "9000"}, {"name": "фэйсайди:", "price": "8500"}, {"name": "заднее стекло:", "price": "6000"}]},
    "12mini_12": {"title": "iPhone 12 mini и 12", "services": [{"name": "акб стандарт:", "price": "4100"}, {"name": "акб фокскон:", "price": "5500"}, {"name": "диспл дешев:", "price": "5000-6000"}, {"name": "диспл средн:", "price": "7000-9000"}, {"name": "диспл дорог:", "price": "10000-13000"}, {"name": "нижний шлейф:", "price": "6500"}, {"name": "камера:", "price": "8000"}, {"name": "фэйсайди:", "price": "8000"}, {"name": "заднее стекло:", "price": "5500"}]},
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

async def device_list(update, context):
    await update.callback_query.edit_message_text("Выберите устройство:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("iPhone", callback_data="modellist")], [InlineKeyboardButton("Назад", callback_data="start")]]))

async def model_list(update, context):
    keyboard = [
        [InlineKeyboardButton("15 Pro и 15 Pro Max", callback_data="model_15pro_15promax"), InlineKeyboardButton("iPhone 15 и 15 Plus", callback_data="model_15_15plus")],
        [InlineKeyboardButton("14 Pro и 14 Pro Max", callback_data="model_14pro_14promax"), InlineKeyboardButton("iPhone 14 и 14 Plus", callback_data="model_14_14plus")],
        [InlineKeyboardButton("13 Pro и 13 Pro Max", callback_data="model_13pro_13promax"), InlineKeyboardButton("iPhone 13 mini и 13", callback_data="model_13mini_13")],
        [InlineKeyboardButton("12 Pro и 12 Pro Max", callback_data="model_12pro_12promax"), InlineKeyboardButton("iPhone 12 mini и 12", callback_data="model_12mini_12")],
        [InlineKeyboardButton("11 Pro и 11 Pro Max", callback_data="model_11pro_11promax"), InlineKeyboardButton("iPhone Xr и 11", callback_data="model_xr_11")],
        [InlineKeyboardButton("iPhone X, Xs и Xs Max", callback_data="model_x_xs_xsmax"), InlineKeyboardButton("iPhone SE 2020 и 2022", callback_data="model_se2020_se2022")],
        [InlineKeyboardButton("Назад", callback_data="devicelist")]
    ]
    await update.callback_query.edit_message_text("Вы выбрали iPhone. Какая модель?", reply_markup=InlineKeyboardMarkup(keyboard))

async def show_price(update, context):
    query = update.callback_query
    model_key = query.data.replace("model_", "")
    data = PRICES.get(model_key)
    text = f"Вы выбрали iPhone — {data['title']}. Что нужно заменить?"
    keyboard = [[InlineKeyboardButton(f"{s['name']} {s['price']}₽", callback_data="book_service")] for s in data['services']]
    keyboard.append([InlineKeyboardButton("Нет моей проблемы", callback_data="book_service")])
    keyboard.append([InlineKeyboardButton("Назад", callback_data="modellist")])
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

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