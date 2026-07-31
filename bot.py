import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

SELL_URL = "https://divar.ir/s/isfahan/buy-apartment"

RENT_URL = "https://divar.ir/s/isfahan/rent-residential/shahrak-milad?business-type=personal%2C&districts=1443%2C1444%2C1446%2C1467%2C1605%2C1606%2C2387&map_bbox=51.652939%2C32.650398%2C51.721099%2C32.735992&map_place_hash=4%7C1442%2C1443%2C1444%2C1446%2C1467%2C1605%2C1606%2C2387%7Capartment-sell%7C"

SUPPORT_PHONE = "09944032954"

def main_keyboard():
return ReplyKeyboardMarkup(
[
["🏠 فروش", "🏠 اجاره منطقه ۷"],
["📞 تماس و پشتیبانی"]
],
resize_keyboard=True
)

def back_keyboard():
return ReplyKeyboardMarkup(
[["↩️ برگشت"]],
resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data.clear()

await update.message.reply_text(
    "🏠 ربات یابنده املاک\n\n"
    "یکی از گزینه‌های زیر را انتخاب کن:",
    reply_markup=main_keyboard()
)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
text = update.message.text

if text == "↩️ برگشت":
    context.user_data.clear()

    await update.message.reply_text(
        "🏠 منوی اصلی\n\n"
        "یکی از گزینه‌ها را انتخاب کن:",
        reply_markup=main_keyboard()
    )
    return

if text == "🏠 فروش":
    await update.message.reply_text(
        "🏠 فایل‌های فروش\n\n"
        "برای مشاهده آگهی‌های فروش روی لینک زیر بزن:\n\n"
        f"{SELL_URL}",
        reply_markup=back_keyboard()
    )
    return

if text == "🏠 اجاره منطقه ۷":
    await update.message.reply_text(
        "🏠 رهن و اجاره منطقه ۷\n\n"
        "برای مشاهده آگهی‌های اجاره روی لینک زیر بزن:\n\n"
        f"{RENT_URL}",
        reply_markup=back_keyboard()
    )
    return

if text == "📞 تماس و پشتیبانی":
    await update.message.reply_text(
        "📞 تماس و پشتیبانی\n\n"
        f"شماره تماس: {SUPPORT_PHONE}\n\n"
        "برای تماس با پشتیبانی می‌توانی با شماره بالا تماس بگیری.",
        reply_markup=back_keyboard()
    )
    return

await update.message.reply_text(
    "لطفاً یکی از گزینه‌های منو را انتخاب کن.",
    reply_markup=main_keyboard()
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

if name == "main":
main()
