import os
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 👉 Вставь сюда свой токен от BotFather
TELEGRAM_TOKEN = "ТОКЕН_ОТ_BOTFATHER"

# Загружаем рецепты
with open("recipes.json", "r", encoding="utf-8") as f:
    recipes = json.load(f)

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Yumbot 🤖🍴 Напиши продукты — я подскажу рецепт!"
    )

# Поиск рецептов
async def find_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_ingredients = set(update.message.text.lower().split())
    selected = None
    for recipe in recipes:
        if user_ingredients & set(recipe["ingredients"]):
            selected = recipe
            break

    if not selected:
        await update.message.reply_text("Упс 😅 Я не нашёл рецепт. Попробуй другие продукты!")
        return

    recipe_text = f"🍽 {selected['name']}\n{recipe['instructions']}"
    await update.message.reply_text(recipe_text)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find_recipe))
    app.run_polling()

if __name__ == "__main__":
    main()
