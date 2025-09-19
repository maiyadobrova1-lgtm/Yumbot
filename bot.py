import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 👉 Твой токен
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# /start — приветствие и меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🔍 Подобрать рецепт по продуктам", "🎲 Случайный рецепт"],
        ["📂 Категории", "⭐ Любимые рецепты"],
        ["🔢 Расчёт калорий", "💬 Поддержка"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Привет! Я Yumbot 🤖🍴\nВыбери, что хочешь сделать:",
        reply_markup=reply_markup
    )

# Обработка кнопок
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🔍 Подобрать рецепт по продуктам":
        await update.message.reply_text("Напиши продукты через пробел, и я подберу рецепт 🥕🥚🍞")
    elif text == "🎲 Случайный рецепт":
        await update.message.reply_text("Хм... случайное блюдо скоро будет тут 😋")
    elif text == "📂 Категории":
        await update.message.reply_text("Категории рецептов скоро будут доступны 📂")
    elif text == "⭐ Любимые рецепты":
        await update.message.reply_text("Ты сможешь сохранять любимые рецепты ⭐ (в разработке)")
    elif text == "🔢 Расчёт калорий":
        await update.message.reply_text("Пришли продукты или фото блюда — я посчитаю калории 🔢 (скоро)")
    elif text == "💬 Поддержка":
        await update.message.reply_text("Напиши свой вопрос сюда: support@yumbot.ai")
    else:
        await update.message.reply_text("Я тебя не понял 🤔 Выбери действие в меню!")

def main():
    if not TELEGRAM_TOKEN:
        raise RuntimeError("⚠️ Укажи TELEGRAM_TOKEN в переменных окружения!")

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()