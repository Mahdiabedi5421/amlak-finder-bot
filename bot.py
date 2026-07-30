import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN", "PASTE_YOUR_BOT_TOKEN_HERE")

AREAS = [
    "برازنده", "اشراق", "آل محمد", "هسا", "کاوه", "غرضی",
    "شاهپسند", "ابوریحان", "گلستان", "شهرک کاوه", "آل یاسین"
]

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 فایل‌های فروش", callback_data="sale")],
        [InlineKeyboardButton("🔑 فایل‌های اجاره", callback_data="rent")],
        [InlineKeyboardButton("🆕 فایل‌های جدید امروز", callback_data="new")],
    ])

def area_menu(kind):
    buttons = []
    for i in range(0, len(AREAS), 2):
        row = []
        for area in AREAS[i:i+2]:
            row.append(InlineKeyboardButton(area, callback_data=f"{kind}:area:{area}"))
        buttons.append(row)
    buttons.append([InlineKeyboardButton("⬅️ برگشت", callback_data="home")])
    return InlineKeyboardMarkup(buttons)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏠 ربات فایل‌یاب املاک\n\nنوع فایل را انتخاب کن:",
        reply_markup=main_menu()
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "home":
        await query.edit_message_text(
            "🏠 ربات فایل‌یاب املاک\n\nنوع فایل را انتخاب کن:",
            reply_markup=main_menu()
        )
        return

    if data in ("sale", "rent"):
        title = "فروش" if data == "sale" else "اجاره"
        await query.edit_message_text(
            f"📌 فایل‌های {title}\n\nمحدوده را انتخاب کن:",
            reply_markup=area_menu(data)
        )
        return

    if data == "new":
        await query.edit_message_text(
            "🆕 فایل‌های جدید امروز\n\n"
            "این بخش در مرحله بعد به جمع‌آوری آگهی‌های واقعی وصل می‌شود.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ برگشت", callback_data="home")]
            ])
        )
        return

    if ":area:" in data:
        kind, _, area = data.partition(":area:")
        title = "فروش" if kind == "sale" else "اجاره"
        await query.edit_message_text(
            f"📍 {area}\n🏷 نوع: {title}\n\n"
            "هنوز منبع آگهی‌ها وصل نشده است.\n"
            "در مرحله بعد، جمع‌آوری مجاز اطلاعات عمومی آگهی‌ها و ذخیره فایل‌ها به این قسمت متصل می‌شود.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ برگشت به نوع فایل", callback_data=kind)],
                [InlineKeyboardButton("🏠 منوی اصلی", callback_data="home")]
            ])
        )

def run():
    logging.basicConfig(level=logging.INFO)
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    run()
