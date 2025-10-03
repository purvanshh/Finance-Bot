import os
import sys

REQUIRED = ["BOT_TOKEN", "GEMINI_API_KEY"]
missing = [k for k in REQUIRED if not os.getenv(k)]
if missing:
    print("ERROR: Missing required environment variables:", ", ".join(missing))
    print("Please set them in your environment or in Render's Dashboard under Environment.")
    sys.exit(1)

print("All required environment variables are present. Starting bot...")
