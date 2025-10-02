How to use environment variables (local only)

1. Copy the example file to create your local `.env` file (do NOT commit `.env`):

   cp .env.example .env

2. Open `.env` and replace placeholders with your real keys.

3. Install `python-dotenv` if you want your Python scripts to automatically load `.env`:

   pip install python-dotenv

4. Update your Python bot code (optional but recommended). At the top of your script add:

   import os
   from dotenv import load_dotenv
   load_dotenv()  # loads variables from .env into environment

   BOT_TOKEN = os.getenv("BOT_TOKEN")
   GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

   # Fallback (optional) if you still have hardcoded values for testing
   # BOT_TOKEN = BOT_TOKEN or "your-fallback-token"
   # GEMINI_API_KEY = GEMINI_API_KEY or "your-fallback-key"

5. Verify locally before pushing to GitHub. Example run (using your venv):

   "/Users/purvansh/Desktop/Finance Bot/.venv/bin/python" "Telegram Phase 3.py"

Notes:
- Keep `.env` out of version control. The `.gitignore` file added to this repo already excludes `.env`.
- Commit and push `.env.example` so others know which variables to set.
- If you want, I can update `Telegram Phase 3.py` to use `os.getenv` and `python-dotenv` for you; tell me and I'll make that change.
