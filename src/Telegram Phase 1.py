import os
from dotenv import load_dotenv
import telebot  # Library to interact with Telegram Bot API

# Load environment variables from a local .env file (if present)
load_dotenv()

# Read Telegram Bot Token from environment for safety
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize the Telegram bot using the provided token
bot = telebot.TeleBot(BOT_TOKEN)

# This handler listens for the /start command.
@bot.message_handler(commands=["start"])
def start(message):
    # Send a simple welcome message to the user
    bot.send_message(message.chat.id, "Hello! Welcome to our simple Telegram bot.")

# Start the bot so it listens for incoming messages
if __name__ == "__main__":
    bot.infinity_polling()
