import os, re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters
from data import PRICES

async def start(update, context):
    context.user_data.clear()
    kb = [[InlineKeyboardButton(cat, callback_data=f"cat_{cat}")] for cat in PRICES.keys()]
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text("Выберите устройство:", reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.message.reply_text("Привет! Эплсин на связи. Выберите устройство:", reply_markup=InlineKeyboardMarkup(kb))

async def model_list(update, context):
    query = update.callback_query
    await query.answer()
    cat = query.data.split("_")[1]
    context.user_data['cat'] = cat
    kb = [[InlineKeyboardButton(data['title'], callback_data=f"mod_{cat}_{m}")] for m, data in PRICES[cat].items()]
    kb.append([InlineKeyboardButton("Назад", callback_data="start")])
    await query.edit_message_text("Выберите модель:", reply_markup=InlineKeyboardMarkup(kb))

async def service_list(update, context):
    query = update.callback_query
    await query.answer()
    _, cat, mod = query.data.split("_")
    context.user_data['mod'] = mod
    kb = [[InlineKeyboardButton(f"{s['name']} {s['price']}₽", callback_data=f"book_{s['name']}")] for s in PRICES[cat][mod]['services']]
    kb.append([InlineKeyboardButton("Назад", callback_data=f"cat_{cat}")])
    await query.edit_message_text(f"Вы выбрали {PRICES[cat][mod]['title']}. Что нужно?", reply_markup=InlineKeyboardMarkup(kb))

async def get_contact(update, context):
    query = update.callback_query
    await query.answer()
    service = query.data.replace("book_", "")
    cat, mod = context.user_data['cat'], context.user_data['mod']
    path = f"{cat} — {PRICES[cat][mod]['title']} — {service}"
    context.user_data['path'] = path
    await query.edit_message_text(f"Вы выбрали: {path}\n\nВведите номер телефона:")

async def final_handler(update, context):
    phone = re.sub(r'\D', '', update.message.text)
    if 10 <= len(phone) <= 11:
        clean_phone = f"+7 ({phone[-10:-7]}) {phone[-7:-4]}-{phone[-4:-2]}-{phone[-2:]}"
        await update.message.reply_text(f"Спасибо! Заявка:\n{context.user_data.get('path')}\nНомер: {clean_phone}")
    else:
        await update.message.reply_text("Ошибка! Введите корректный номер (10-11 цифр).")

app = Application.builder().token(os.environ["TOKEN"]).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(start, pattern="start")) 
app.add_handler(CallbackQueryHandler(model_list, pattern="cat_"))
app.add_handler(CallbackQueryHandler(service_list, pattern="mod_"))
app.add_handler(CallbackQueryHandler(get_contact, pattern="book_"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, final_handler))

if __name__ == "__main__":
    print("--- ЗАПУСК БОТА ---")
    try:
        from data import PRICES
        print(f"База данных успешно загружена. Ключи: {list(PRICES.keys())}")
        
        # Добавляем хендлеры
        app = Application.builder().token(os.environ["TOKEN"]).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(start, pattern="start"))
        app.add_handler(CallbackQueryHandler(model_list, pattern="cat_"))
        app.add_handler(CallbackQueryHandler(service_list, pattern="mod_"))
        app.add_handler(CallbackQueryHandler(get_contact, pattern="book_"))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, final_handler))
        
        print("Хендлеры добавлены. Начинаем опрос...")
        app.run_polling()
    except Exception as e:
        print(f"КРИТИЧЕСКАЯ ОШИБКА ПРИ ЗАПУСКЕ: {e}")
