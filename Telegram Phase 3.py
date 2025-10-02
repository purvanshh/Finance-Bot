import os
from dotenv import load_dotenv
import telebot                           # Telegram Bot API library
import google.generativeai as genai        # Google GenAI for generating content

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

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id  # Unique identifier for the user
    user_data[user_id] = {}    # Initialize an empty dictionary for storing user inputs

    # Welcome message with an introduction to the financial planning bot
    bot.send_message(
        user_id,
        "Welcome to Finance Bot!\n"
        "Let’s create a personalized financial plan for you.\n\n"
        "First, share your age:"
    )
    # Set the next handler to capture the age
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    user_id = message.chat.id
    user_data[user_id]["age"] = message.text  # Store the user's age
    bot.send_message(user_id, "💸 What is your monthly income (in ₹)?")
    bot.register_next_step_handler(message, get_income)

def get_income(message):
    user_id = message.chat.id
    user_data[user_id]["income"] = message.text  # Store the monthly income
    bot.send_message(user_id, "What are your monthly expenses (in ₹)?")
    bot.register_next_step_handler(message, get_expenses)

def get_expenses(message):
    user_id = message.chat.id
    user_data[user_id]["expenses"] = message.text  # Store the monthly expenses
    bot.send_message(
        user_id,
        "What are your financial goals?\n"
        "(e.g., Buy a home, Child’s education, Retirement, Tax saving):"
    )
    bot.register_next_step_handler(message, get_goals)

def get_goals(message):
    user_id = message.chat.id
    user_data[user_id]["goals"] = message.text  # Store the financial goals

    # Retrieve all collected data for this user
    data = user_data[user_id]

    # Build a detailed prompt for the GenAI model
    prompt = f"""
    Act as a certified Indian financial advisor. Create a personalized plan for a {data['age']}-year-old with:
    - Monthly income: ₹{data['income']}
    - Monthly expenses: ₹{data['expenses']}
    - Financial goals: {data['goals']}

    Provide advice tailored to an Indian citizen, taking into account the current income, expenses and future financial goals. You can suggest the following:
    1. Savings Potential: Calculate how much the user can save monthly.
    2. Feasibility of Financial Goals: Assess whether the goal is realistic based on income and savings.
    3. Investment Recommendations: Suggest suitable investment options based on affordability.
    4. Budget Optimization: Provide recommendations to cut unnecessary expenses and increase savings.
    5. Action Plan with Timelines: Guide the user with a step-by-step approach to achieving their financial goal.
   
     Use ₹ currency, and terms like 'lakh'/'crore'. Avoid jargon. Give in a format that telegram bot can display properly.
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
        else:
            bot.send_message(user_id, "⚠️ No response generated. Please try again!")
            
    except Exception as e:
        # If there is an error during content generation, notify the user with more details
        print(f"Error generating advice for user {user_id}: {str(e)}")
        bot.send_message(user_id, f"⚠️ Error generating advice: {str(e)}\n\nPlease try again or contact support if this persists.")

if __name__ == "__main__":
    bot.infinity_polling()
