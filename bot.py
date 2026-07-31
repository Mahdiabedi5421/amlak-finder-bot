import os
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
DIVAR_API_KEY = os.getenv("DIVAR_API_KEY")

AREAS = [
    "برازنده", "اشراق", "آل محمد", "هسا",
    "کاوه", "غرضی", "شاهپسند", "ابوریحان",
    "گلستان", "شهرک کاوه", "آل یاسین"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🏠 فروش", "🏠 اجاره"]]

    await update.message.reply_text(
        "🏠 ربات یابنده املاک\n\n"
        "نوع فایل را انتخاب کن:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text in ["🏠 فروش", "🏠 اجاره"]:
        context.user_data["type"] = "فروش" if text == "🏠 فروش" else "اجاره"

        keyboard = [
            ["برازنده", "اشراق", "آل محمد"],
            ["هسا", "کاوه", "غرضی"],
            ["شاهپسند", "ابوریحان", "گلستان"],
            ["شهرک کاوه", "آل یاسین"]
        ]

        await update.message.reply_text(
            f"نوع فایل: {context.user_data['type']}\n\n"
            "محدوده را انتخاب کن:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )

    elif text in AREAS:
        file_type = context.user_data.get("type", "فروش")

        await update.message.reply_text(
            f"🔎 در حال جست‌وجوی آگهی‌های {file_type} در محدوده {text}..."
        )

        if not DIVAR_API_KEY:
            await update.message.reply_text(
                "❌ کلید API دیوار در تنظیمات ربات پیدا نشد."
            )
            return

        await update.message.reply_text(
            "✅ کلید API پیدا شد.\n\n"
            "مرحله اتصال به سرویس جست‌وجوی دیوار آماده است."
        )

    else:
        await update.message.reply_text(
            "لطفاً یکی از گزینه‌های منو را انتخاب کن."
        )


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN تنظیم نشده است.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )

    print("ربات اجرا شد...")
    app.run_polling()


if __name__ == "__main__":
    main()
