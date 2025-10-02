Finance Bot — Telegram AI Financial Advisor
=========================================

This repository contains a simple Telegram AI Financial Advisor bot that uses Google Generative AI (Gemini) to generate personalized financial guidance.

Files of interest
- `Telegram Phase 1.py` — minimal bot example
- `Telegram Phase 2.py` — collects user inputs and echoes them
- `Telegram Phase 3.py` — AI-integrated bot (uses Gemini)
- `Telegram Phase 3 Fixed.py` — improved/short-response + message-splitting version (recommended)
- `test_gemini.py` — quick API key connectivity test for Gemini
- `list_models.py` — lists available Gemini models (useful for picking a model name)
- `.env.example` — example environment variables (copy to `.env` locally)
- `requirements.txt` — Python dependencies

Quick overview
-------------
1. Put your secrets locally in a `.env` file (do NOT commit it).
2. Install dependencies into a virtual environment.
3. Run `Telegram Phase 3 Fixed.py` to start the bot.

Prerequisites
-------------
- Python 3.8+ (this project was tested with Python 3.9.6 in the workspace)
- A Telegram Bot token (from BotFather)
- A Google Gemini API key

Setup (macOS / zsh)
-------------------
Open a terminal and run the following commands from the project root (`/Users/purvansh/Desktop/Finance Bot`):

Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` file from the example and add your keys:

```bash
cp .env.example .env
# then edit .env and paste your real keys
# BOT_TOKEN=your-real-telegram-token
# GEMINI_API_KEY=your-real-gemini-key
```

Important: `.env` is included in `.gitignore` so it will not be committed.

Running the bot
---------------
From the project root (with the venv activated):

Run the recommended fixed version:

```bash
python "Telegram Phase 3 Fixed.py"
```

Or run the main Phase 3 script:

```bash
python "Telegram Phase 3.py"
```

Note: If your path contains spaces (like the example path), quoting the script path ensures it runs correctly.

Testing Gemini connectivity
--------------------------
If you want to test your Gemini API key quickly before running the bot:

```bash
python test_gemini.py
```

If everything is configured correctly you should see a short response in the terminal.

Listing available models
------------------------
To see which Gemini models are available and which support generation:

```bash
python list_models.py
```

Security and deployment notes
-----------------------------
- Never commit your `.env` file to version control. Only commit `.env.example`.
- For deployments (Heroku, Docker, cloud VMs, GitHub Actions), set the BOT_TOKEN and GEMINI_API_KEY as environment variables in the host environment / CI secrets.

Running the bot in background
----------------------------
To run the bot detached from the terminal (simple approach):

```bash
nohup python "Telegram Phase 3 Fixed.py" > bot.log 2>&1 &
```

Or use `screen`, `tmux`, or a process manager (systemd, PM2, supervisord) for production.

Troubleshooting
---------------
- If you see: `Bad Request: message is too long` — use `Telegram Phase 3 Fixed.py` which requests shorter responses and splits long messages automatically.
- If you see `models/... is not found` errors — run `list_models.py` to pick a supported model and update `Telegram Phase 3.py` or `Telegram Phase 3 Fixed.py` to use that model string when creating `genai.GenerativeModel(...)`.
- If the bot fails to import `dotenv`, install dependencies with `pip install -r requirements.txt`.

Need help?
----------
If you'd like, I can:
- Update your scripts to assert that the required env vars are present and print a friendly message if missing.
- Add a small `pre-run` checker script that ensures `BOT_TOKEN` and `GEMINI_API_KEY` are set before starting the bot.

Creating a Telegram Bot (BotFather)
-----------------------------------

1. Open Telegram and search for the official BotFather (@BotFather).
2. Start a chat and send the command `/newbot`.
3. Follow the prompts:
   - Choose a display name for your bot (e.g., "Finance Advisor Bot").
   - Choose a username for the bot that ends with `bot` (e.g., `finance_advisor_bot`).
4. BotFather will return a **Bot Token** that looks like `123456789:ABCDefGhIjKlmNoPQRsTuVwXyZ`.
   - Copy the token and put it into your local `.env` as `BOT_TOKEN=...`.
5. (Optional) Configure the bot’s profile picture and description using BotFather commands like `/setuserpic`, `/setdescription` and `/setabouttext`.

Tips and webhooks vs polling

- The example scripts use `bot.infinity_polling()` which is simple and works for small projects and development.
- For production (higher reliability and scale), consider setting a webhook and running your bot behind an HTTPS endpoint (e.g., using a small web server or a cloud function). You can configure a webhook URL with BotFather using `/setwebhook`.

Permissions and privacy

- If you want the bot to be able to read messages in groups, add it to the group and give appropriate permissions. For private chats it can read messages directed to it.
- Review Telegram’s Bot API docs for message limits and best practices: https://core.telegram.org/bots/api

Security reminder

- Keep your Bot Token secret. Treat it like any other credential. Do not commit it to your repository.

