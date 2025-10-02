import os
from dotenv import load_dotenv
import telebot  # Library to interact with Telegram Bot API

# Load environment variables from a local .env file (if present)
load_dotenv()

# Read Telegram Bot Token from environment for safety
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Dictionary to store data from different users during the conversation.
user_data = {}

# Start the conversation when the user sends /start.
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id  # Unique ID for the user
    user_data[user_id] = {}    # Initialize an empty data dictionary for this user

    # Send a welcome message and ask for the user's age
    bot.send_message(
        user_id,
        "Welcome! Let's begin our conversation.\n\nPlease tell me your age:"
    )
    # Register the next handler to process the user's age
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    user_id = message.chat.id
    user_data[user_id]["age"] = message.text  # Save the user's age
    bot.send_message(user_id, "Great! What is your monthly income (in ₹)?")
    bot.register_next_step_handler(message, get_income)

def get_income(message):
    user_id = message.chat.id
    user_data[user_id]["income"] = message.text  # Save the monthly income
    bot.send_message(user_id, "Thanks! Now, what are your monthly expenses (in ₹)?")
    bot.register_next_step_handler(message, get_expenses)

def get_expenses(message):
    user_id = message.chat.id
    user_data[user_id]["expenses"] = message.text  # Save the monthly expenses
    bot.send_message(
        user_id,
        "Finally, please share your financial goals (e.g., Buy a home, Retirement, Tax saving):"
    )
    bot.register_next_step_handler(message, finish_conversation)

def finish_conversation(message):
    user_id = message.chat.id
    user_data[user_id]["goals"] = message.text  # Save the financial goals

    # Echo the collected data back to the user for confirmation
    summary = (
        f"Here is what we've gathered:\n"
        f"Age: {user_data[user_id]['age']}\n"
        f"Monthly Income: ₹{user_data[user_id]['income']}\n"
        f"Monthly Expenses: ₹{user_data[user_id]['expenses']}\n"
        f"Financial Goals: {user_data[user_id]['goals']}"
    )
    bot.send_message(user_id, summary)

if __name__ == "__main__":
    bot.infinity_polling()
