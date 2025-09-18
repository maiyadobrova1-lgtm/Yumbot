import os
import json
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 👉 Токен Telegram (лучше хранить в переменных окружения)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Загружаем рецепты из файла
with open("recipes.json", "r", encoding="utf-8") as f:
    recipes = json.load(f)

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Yumbot 🤖🍴\n"
        "Напиши продукты через пробел, и я подскажу рецепт!"
    )

# Поиск картинки через API TheMealDB
def get_mealdb_image(recipe_name: str):
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={recipe_name}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data["meals"]:
            return data["meals"][0]["strMealThumb"]
    except Exception as e:
        print(f"[Image error] {e}")
    return None

# Поиск рецепта по ингредиентам
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

    recipe_text = f"🍽 {selected['name']}\n\n{selected['instructions']}"

    # ищем картинку
    image_url = get_mealdb_image(selected["name"])
    if image_url:
        await update.message.reply_photo(photo=image_url, caption=recipe_text)
    else:
        await update.message.reply_text(recipe_text)

# Запуск бота
def main():
    if not TELEGRAM_TOKEN:
        raise RuntimeError("⚠️ Добавь TELEGRAM_TOKEN в переменные окружения!")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find_recipe))
    app.run_polling()

if __name__ == "__main__":
    main()
