import os
from dotenv import load_dotenv
import telebot                           # Telegram Bot API library
import google.generativeai as genai        # Google GenAI for generating content
from flask import Flask
import threading
import time

# Load local .env if present and read keys from environment
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the Telegram bot and Google GenAI model
bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# Dictionary to store conversation data for each user
user_data = {}

# Function to split long messages for Telegram
def split_message(text, max_length=4000):
    """Split long messages into chunks that fit Telegram's limit"""
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    # Split by sentences or lines
    lines = text.split('\n')
    
    for line in lines:
        if len(current_chunk + line + '\n') <= max_length:
            current_chunk += line + '\n'
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = line + '\n'
            else:
                # If single line is too long, split it
                words = line.split(' ')
                for word in words:
                    if len(current_chunk + word + ' ') <= max_length:
                        current_chunk += word + ' '
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                            current_chunk = word + ' '
                        else:
                            chunks.append(word)
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks


def is_conversation_active(user_id):
    """Return True if the user has an active session stored in user_data."""
    return user_id in user_data

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id  # Unique identifier for the user
    # initialize session with timestamp and state
    user_data[user_id] = {"_ts": time.time(), "state": "awaiting_age"}

    # Welcome message with an introduction to the financial planning bot
    bot.send_message(
        user_id,
        "Welcome to Finance Bot!\n"
        "Let's create a personalized financial plan for you.\n\n"
        "First, share your age:"
    )
    # Set the next handler to capture the age
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    user_id = message.chat.id
    # ignore if there's no active session (user may have cancelled)
    if not is_conversation_active(user_id):
        bot.send_message(user_id, "No active session. Send /start to begin a new one.")
        return

    # update timestamp and state
    user_data.setdefault(user_id, {})
    user_data[user_id]["_ts"] = time.time()
    user_data[user_id]["state"] = "awaiting_income"
    user_data[user_id]["age"] = message.text  # Store the user's age

    bot.send_message(user_id, "💸 What is your monthly income (in ₹)?")
    bot.register_next_step_handler(message, get_income)

def get_income(message):
    user_id = message.chat.id
    if not is_conversation_active(user_id):
        bot.send_message(user_id, "No active session. Send /start to begin a new one.")
        return

    user_data.setdefault(user_id, {})
    user_data[user_id]["_ts"] = time.time()
    user_data[user_id]["state"] = "awaiting_expenses"
    user_data[user_id]["income"] = message.text  # Store the monthly income

    bot.send_message(user_id, "What are your monthly expenses (in ₹)?")
    bot.register_next_step_handler(message, get_expenses)

def get_expenses(message):
    user_id = message.chat.id
    if not is_conversation_active(user_id):
        bot.send_message(user_id, "No active session. Send /start to begin a new one.")
        return

    user_data.setdefault(user_id, {})
    user_data[user_id]["_ts"] = time.time()
    user_data[user_id]["state"] = "awaiting_goals"
    user_data[user_id]["expenses"] = message.text  # Store the monthly expenses

    bot.send_message(
        user_id,
        "What are your financial goals?\n"
        "(e.g., Buy a home, Child's education, Retirement, Tax saving):"
    )
    bot.register_next_step_handler(message, get_goals)

def get_goals(message):
    user_id = message.chat.id
    if not is_conversation_active(user_id):
        bot.send_message(user_id, "No active session. Send /start to begin a new one.")
        return

    user_data.setdefault(user_id, {})
    user_data[user_id]["_ts"] = time.time()
    user_data[user_id]["state"] = "generating_advice"
    user_data[user_id]["goals"] = message.text  # Store the financial goals

    # Retrieve all collected data for this user
    data = user_data[user_id]

    # Calculate savings if possible
    try:
        savings = int(data['income']) - int(data['expenses'])
    except:
        savings = "Calculate manually"

    # Build a concise prompt for the GenAI model
    prompt = f"""
    Act as a certified Indian financial advisor. Create a CONCISE personalized plan for a {data['age']}-year-old with:
    - Monthly income: ₹{data['income']}
    - Monthly expenses: ₹{data['expenses']}  
    - Financial goals: {data['goals']}

    Provide SHORT advice (max 2000 characters) with:
    1. Monthly Savings: ₹{savings}
    2. Goal Feasibility: Quick assessment
    3. Top 2 Investment Options: Brief suggestions  
    4. Budget Tip: One key recommendation
    5. Action Plan: 3 simple steps

    Keep it brief, use ₹ currency, avoid jargon. Format for Telegram (max 2000 chars).
    """

    try:
        # Send a processing message to the user
        bot.send_message(user_id, "🤖 Analyzing your financial data and generating personalized advice... Please wait a moment.")
        
        # Generate personalized financial advice using the GenAI model
        response = model.generate_content(prompt)
        
        # Check if response has content
        if response and response.text:
            # Split the response into manageable chunks
            full_response = f"📊 Your India-Focused Financial Plan\n\n{response.text}"
            message_chunks = split_message(full_response)
            
            # Send each chunk as a separate message
            for i, chunk in enumerate(message_chunks):
                if i == 0:
                    bot.send_message(user_id, chunk)
                else:
                    bot.send_message(user_id, f"📊 Continued...\n\n{chunk}")

            # Conversation finished: clear session and confirm
            user_data.pop(user_id, None)
            bot.send_message(user_id, "✅ Done. Send /start if you want another personalized plan.")
        else:
            bot.send_message(user_id, "⚠️ No response generated. Please try again!")
            
    except Exception as e:
        # If there is an error during content generation, notify the user with more details
        print(f"Error generating advice for user {user_id}: {str(e)}")
        bot.send_message(user_id, f"⚠️ Error generating advice: {str(e)}\n\nPlease try again or contact support if this persists.")


@bot.message_handler(commands=["cancel", "end", "stop"])
def cancel_conversation(message):
    user_id = message.chat.id
    if user_data.pop(user_id, None):
        bot.send_message(user_id, "🛑 Conversation ended. Send /start whenever you're ready to begin again.")
    else:
        bot.send_message(user_id, "No active conversation. Send /start to begin a new one.")

def run_bot():
    bot.infinity_polling()

app = Flask(__name__)

@app.route("/")
def health():
    return "Finance Bot is running"

if __name__ == "__main__":
    # Start background cleanup thread to remove stale sessions
    def cleanup_sessions(expiry_seconds=600, sleep_seconds=60):
        while True:
            now = time.time()
            for uid, data in list(user_data.items()):
                ts = data.get('_ts')
                if ts and now - ts > expiry_seconds:
                    user_data.pop(uid, None)
                    try:
                        bot.send_message(uid, "⏳ Your session timed out due to inactivity. Send /start to begin again.")
                    except Exception:
                        pass
            time.sleep(sleep_seconds)

    cleanup_thread = threading.Thread(target=cleanup_sessions, daemon=True)
    cleanup_thread.start()

    # Start bot in background thread
    t = threading.Thread(target=run_bot, daemon=True)
    t.start()

    # Run the Flask web server on the port Render provides
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
