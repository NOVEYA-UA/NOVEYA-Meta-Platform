
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

class TelegramGateway:

    def __init__(self, token, regulator):
        self.token = token
        self.regulator = regulator

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f"RANK: {self.regulator.last_result}")

    async def run_cycle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.regulator.run_cycle()
        await update.message.reply_text("Cycle executed")

    def start(self):
        app = ApplicationBuilder().token(self.token).build()
        app.add_handler(CommandHandler("status", self.status))
        app.add_handler(CommandHandler("run", self.run_cycle))
        app.run_polling()
