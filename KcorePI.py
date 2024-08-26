from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

with open('token.txt', 'r') as file:
    token = file.read().strip()

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("hello", hello))

app.run_polling()
