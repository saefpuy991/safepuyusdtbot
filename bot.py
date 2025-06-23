import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users[user_id] = {
        'deposit_made': False,
        'level': 0,
        'balance': 0,
        'referrals': 0,
        'earned_from_referrals': 0,
    }
    await update.message.reply_text(
        "أهلاً بك في SafePay USDT Bot!\n"
        "لتفعيل حسابك، يجب أن تقوم بإيداع 13 دولار على الأقل.\n"
        "BNB: 0x2c281bd14ae21d0956fa81f70c6eaadc79371441\n"
        "TRC20: TLcjgAUz3zrmzX9bNTTQWfia1VWEDXxvZZ\n"
        "بعد الإيداع، استخدم /verify لإثبات الدفع."
    )

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = users.get(user_id)
    if not user:
        await update.message.reply_text("يرجى بدء المحادثة أولاً باستخدام /start")
        return
    if user['deposit_made']:
        await update.message.reply_text("حسابك مفعل بالفعل.")
        return

    user['deposit_made'] = True
    user['level'] = 1
    user['balance'] = 0
    await update.message.reply_text(
        "تم تفعيل حسابك بنجاح! أنت الآن في المستوى 1 وتربح 4.5 دولار يومياً.\n"
        "استخدم /tasks لعرض المهام اليومية."
    )

async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = users.get(user_id)
    if not user or not user['deposit_made']:
        await update.message.reply_text("يرجى تفعيل حسابك أولاً عبر /verify")
        return
    await update.message.reply_text(
        "مهمتك لليوم:\n"
        "شارك رابط الإحالة الخاص بك مع أصدقائك لتحصل على 1 USDT عن كل إحالة ناجحة.\n"
        f"رابط الإحالة: https://t.me/YourBotUsername?start={user_id}"
    )

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = users.get(user_id)
    if not user:
        await update.message.reply_text("يرجى بدء المحادثة أولاً باستخدام /start")
        return
    await update.message.reply_text(
        f"رصيدك الحالي: {user['balance']} USDT\n"
        f"مكافآت الإحالات: {user['earned_from_referrals']} USDT\n"
        f"مستواك الحالي: {user['level']}"
    )

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = users.get(user_id)
    if not user or user['balance'] < 4:
        await update.message.reply_text(
            "رصيدك غير كافٍ للسحب. الحد الأدنى للسحب هو 4 USDT."
        )
        return
    await update.message.reply_text(
        "تم استلام طلب السحب. سيتم التحويل خلال 1 إلى 5 دقائق، أو حتى ساعات حسب الضغط."
    )
    user['balance'] = 0

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("verify", verify))
    app.add_handler(CommandHandler("tasks", tasks))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("withdraw", withdraw))
    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()
