"""
Config: Bot Settings — Behavior, stealth, and performance tuning
"""

# ────────────────────────────────────────────────────────────────
# 🌐 BROWSER SETTINGS
# ────────────────────────────────────────────────────────────────

# Use stealth mode (undetected-chromedriver) to avoid bot detection
stealth_mode = True

# Run browser in background (headless mode)
# Set False to see what the bot is doing in real-time
run_in_background = False

# Chrome profile path (for persistent sessions)
chrome_profile_path = "chrome_profile"

# ────────────────────────────────────────────────────────────────
# ⏱️ TIMING & DELAYS (seconds)
# ────────────────────────────────────────────────────────────────

# Delays are randomized between min and max to appear human-like
min_click_delay = 0.5          # Minimum delay between clicks
max_click_delay = 2.0          # Maximum delay between clicks

min_typing_delay = 0.03        # Minimum delay between keystrokes
max_typing_delay = 0.12        # Maximum delay between keystrokes

page_load_timeout = 15         # Max wait for page load (seconds)
element_wait_timeout = 10      # Max wait for element to appear

# Delay between applications (seconds)
min_application_delay = 3
max_application_delay = 8

# ────────────────────────────────────────────────────────────────
# 🔄 SESSION MANAGEMENT
# ────────────────────────────────────────────────────────────────

# Keep screen awake during automation (prevents sleep)
keep_screen_awake = True

# Auto-save applied jobs to JSON after each successful application
auto_save_applied_jobs = True

# Log level: "DEBUG", "INFO", "WARNING", "ERROR"
log_level = "INFO"

# Log file directory
log_directory = "logs/"

# ────────────────────────────────────────────────────────────────
# 🤖 AI SETTINGS
# ────────────────────────────────────────────────────────────────

# Generate AI-tailored resume for each job?
ai_resume_customization = False

# Generate AI cover letter for each job?
ai_cover_letter = False

# Extract skills from job description using AI?
ai_skill_extraction = True

# AI resume output directory
ai_resume_output_dir = "generated_resumes/"

# ────────────────────────────────────────────────────────────────
# 📊 DASHBOARD SETTINGS
# ────────────────────────────────────────────────────────────────

# Enable web dashboard for viewing application history?
enable_dashboard = True

# Dashboard port
dashboard_port = 5000

# ────────────────────────────────────────────────────────────────
# 🔒 SAFETY
# ────────────────────────────────────────────────────────────────

# Safe mode — extra checks before each action
safe_mode = False

# Follow companies when applying? (LinkedIn option)
follow_company_on_apply = False
