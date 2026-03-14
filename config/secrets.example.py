"""
Config: Secrets — LinkedIn credentials & API keys
⚠️ This file is GITIGNORED — never push it to GitHub!
"""

# ────────────────────────────────────────────────────────────────
# 🔐 LINKEDIN CREDENTIALS
# ────────────────────────────────────────────────────────────────

# If left empty, bot will use saved Chrome profile session
# If profile session expired, it will ask you to login manually
linkedin_email = ""
linkedin_password = ""

# ────────────────────────────────────────────────────────────────
# 🤖 OPENAI API KEY (Optional — for AI features)
# ────────────────────────────────────────────────────────────────

# Used for:
# - AI-powered resume customization per job
# - Smart answer generation for unknown questions
# - Auto-generated cover letters
# Get your key: https://platform.openai.com/api-keys
openai_api_key = ""

# Model to use (gpt-4, gpt-3.5-turbo, etc.)
openai_model = "gpt-4"
