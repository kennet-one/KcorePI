from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import asyncio

# ініціалізаця планіровщика
scheduler = BackgroundScheduler()
scheduler.start()

with open('token.txt', 'r') as file:
    token = file.read().strip()

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

# функція для відправки запланованого повідомлення
async def send_scheduled_message(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message: str):
    await context.bot.send_message(chat_id=chat_id, text=message)

# синхронна функція для запуску асинхроного коду
def run_async(coroutine):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(coroutine)
    loop.close()

# команда для налаштування повідомлення
async def schedule_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # очікуемо формат команди: /schedule YYYY-MM-DD HH:MM текст повідомлення
        time = datetime.strptime(context.args[0] + " " + context.args[1], '%Y-%m-%d %H:%M')
        message = " ".join(context.args[2:])
        
        chat_id = update.message.chat_id
        # додаемо завдання в планувальник
        scheduler.add_job(run_async, 'date', run_date=time, args=[send_scheduled_message(context, chat_id, message)])
        
        await context.bot.send_message(chat_id=chat_id, text=f"'{message}' на {time}")   # фітбек шо на коли записано
    except (IndexError, ValueError):
        await context.bot.send_message(chat_id=update.message.chat_id, text="Usage: /schedule YYYY-MM-DD HH:MM:SS пройобано")

app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("schedule", schedule_message))

app.run_polling()