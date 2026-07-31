import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

AREAS = [
    "برازنده", "اشراق", "آل محمد", "هسا",
    "کاوه", "غرضی", "شاهپسند", "ابوریحان",
    "گلستان", "شهرک کاوه", "آل یاسین"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🏠 فروش", "🏠 اجاره"]
    ]

    await update.message.reply_text(
        "سلام 👋\n"
        "به ربات یابنده املاک خوش آمدی.\n\n"
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
            "حالا محدوده را انتخاب کن:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )

    elif text in AREAS:
        file_type = context.user_data.get("type", "فروش")

        await update.message.reply_text(
            f"✅ انتخاب شد\n\n"
            f"نوع فایل: {file_type}\n"
            f"محدوده: {text}\n\n"
            "🔎 بخش دریافت آگهی‌ها در مرحله بعد به این قسمت متصل می‌شود."
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
        MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)
    )

    print("ربات اجرا شد...")
    app.run_polling()


if __name__ == "__main__":
    main()
