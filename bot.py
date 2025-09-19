import os
import json
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 👉 Твой Telegram токен (лучше хранить в переменной окружения)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "ВСТАВЬ_СВОЙ_ТОКЕН")

# Загружаем рецепты из файла
with open("recipes.json", "r", encoding="utf-8") as f:
    recipes = json.load(f)

# --- Команды ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🍳 Подобрать рецепт", "🎲 Случайное блюдо"],
        ["📂 Категории", "⭐ Избранное"],
        ["📞 Поддержка", "🔥 Калории"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Привет! Я Yumbot 🤖🍴\nВыбери, что хочешь сделать:",
        reply_markup=reply_markup
    )

async def find_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_ingredients = set(update.message.text.lower().split())
    selected = None
    for recipe in recipes:
        if user_ingredients & set(recipe["ingredients"]):
            selected = recipe
            break

    if not selected:
        await update.message.reply_text("😅 Не нашёл рецепт. Попробуй другие продукты!")
        return

    recipe_text = f"🍽 {selected['name']}\n{selected['instructions']}"

    # для примера — картинка через MealDB
    image_url = get_mealdb_image(selected["name"])
    if image_url:
        await update.message.reply_photo(photo=image_url, caption=recipe_text)
    else:
        await update.message.reply_text(recipe_text)

# --- Вспомогательная функция ---
def get_mealdb_image(recipe_name: str):
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={recipe_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["meals"]:
            return data["meals"][0]["strMealThumb"]
    return None

# --- Запуск бота ---
def main():
    if TELEGRAM_TOKEN == "ВСТАВЬ_СВОЙ_ТОКЕН":
        raise RuntimeError("⚠️ Вставь свой Telegram-токен в bot.py или переменные окружения!")

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find_recipe))

    app.run_polling()

if __name__ == "__main__":
    main()