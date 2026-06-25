import os, re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters
from price import PRICES
from text import MESSAGES

async def start(update, context):
    context.user_data.clear()
    kb = [[InlineKeyboardButton(cat, callback_data=f"cat_{cat}")] for cat in PRICES.keys()]
    
    photo_path = 'start.webp'
    
    if update.callback_query:
        await update.callback_query.answer()
        try:
            with open(photo_path, 'rb') as photo:
                await update.callback_query.edit_message_media(
                    media=InputMediaPhoto(media=photo, caption=MESSAGES["start"], parse_mode='HTML'),
                    reply_markup=InlineKeyboardMarkup(kb)
                )
        except FileNotFoundError:
            await update.callback_query.edit_message_text(MESSAGES["start"], reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')
    else:
        try:
            with open(photo_path, 'rb') as photo:
                await update.message.reply_photo(photo=photo, caption=MESSAGES["start"], reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')
        except FileNotFoundError:
            await update.message.reply_text(MESSAGES["start"], reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')

async def model_list(update, context):
    query = update.callback_query
    await query.answer()
    cat = query.data.split("_", 1)[1]
    context.user_data['cat'] = cat
    kb = [[InlineKeyboardButton(data['title'], callback_data=f"mod_{cat}_{m}")] for m, data in PRICES[cat].items()]
    kb.append([InlineKeyboardButton("Назад", callback_data="start")])
    await query.edit_message_text(MESSAGES["choose_model"].format(cat=cat), reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')

async def service_list(update, context):
    query = update.callback_query
    await query.answer()
    raw_data = query.data.replace("mod_", "", 1)
    cat, mod = raw_data.split("_", 1)
    context.user_data['cat'] = cat
    context.user_data['mod'] = mod
    
    kb = [[InlineKeyboardButton(f"{s['name']} {s['price']}₽", callback_data=f"book_{s['name']}")] for s in PRICES[cat][mod]['services']]
    
    # Добавляем "Нет моей проблемы" и "Назад"
    kb.append([InlineKeyboardButton("Нет моей проблемы", callback_data="book_another_problem")])
    kb.append([InlineKeyboardButton("Назад", callback_data=f"cat_{cat}")])
    
    await query.edit_message_text(MESSAGES["choose_service"].format(title=PRICES[cat][mod]['title']), reply_markup=InlineKeyboardMarkup(kb), parse_mode='HTML')

async def get_contact(update, context):
    query = update.callback_query
    await query.answer()
    service = query.data.replace("book_", "", 1)
    cat, mod = context.user_data['cat'], context.user_data['mod']
    
    if service == "another_problem":
        path = f"{cat} — {PRICES[cat][mod]['title']} — Другая проблема"
    else:
        path = f"{cat} — {PRICES[cat][mod]['title']} — {service}"
        
    context.user_data['path'] = path
    await query.edit_message_text(MESSAGES["get_contact"].format(path=path), parse_mode='HTML')

async def final_handler(update, context):
    phone = re.sub(r'\D', '', update.message.text)
    if 10 <= len(phone) <= 11:
        clean_phone = f"+7 ({phone[-10:-7]}) {phone[-7:-4]}-{phone[-4:-2]}-{phone[-2:]}"
        await update.message.reply_text(MESSAGES["success"].format(path=context.user_data.get('path'), phone=clean_phone), parse_mode='HTML')
    else:
        await update.message.reply_text(MESSAGES["error_phone"], parse_mode='HTML')

if __name__ == "__main__":
    app = Application.builder().token(os.environ["TOKEN"]).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(start, pattern="^start$"))
    app.add_handler(CallbackQueryHandler(model_list, pattern="^cat_"))
    app.add_handler(CallbackQueryHandler(service_list, pattern="^mod_"))
    app.add_handler(CallbackQueryHandler(get_contact, pattern="^book_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, final_handler))
    app.run_polling()
