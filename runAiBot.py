#!/usr/bin/env python3
"""
LinkedIn AI Auto Job Applier — Entry Point
Run this to start the bot.

Usage:
    python runAiBot.py
"""

import sys
import os

try:
    from pyfiglet import figlet_format
    from colorama import init, Fore, Style
    init()
    HAS_COLORS = True
except ImportError:
    HAS_COLORS = False


def print_banner():
    """Print the startup banner."""
    if HAS_COLORS:
        print(Fore.CYAN)
        print(figlet_format("LinkedIn AI", font="slant"))
        print(f"{Fore.WHITE}  Auto Job Applier v1.0")
        print(f"  {'─' * 50}")
        print(f"  {Fore.GREEN}Author:{Fore.WHITE} Rayees Yousuf")
        print(f"  {Fore.GREEN}GitHub:{Fore.WHITE} github.com/RayeesYousufGenAi")
        print(f"  {'─' * 50}")
        print(Style.RESET_ALL)
    else:
        print("=" * 55)
        print("  LinkedIn AI Auto Job Applier v1.0")
        print("  Author: Rayees Yousuf")
        print("=" * 55)


def check_config():
    """Verify configuration files exist."""
    required = [
        "config/personals.py",
        "config/search.py",
        "config/questions.py",
        "config/settings.py",
    ]

    missing = [f for f in required if not os.path.exists(f)]
    if missing:
        print(f"\n❌ Missing config files: {', '.join(missing)}")
        print("   Please configure all files in the /config directory")
        return False

    # Check for secrets
    if not os.path.exists("config/secrets.py"):
        print("\n⚠️  config/secrets.py not found!")
        print("   Copy config/secrets.example.py → config/secrets.py")
        print("   Then add your LinkedIn credentials (optional) and OpenAI key (optional)")

        response = input("\n   Continue without credentials? The bot will ask for manual login. (y/n): ")
        if response.lower() != "y":
            return False

        # Create empty secrets file
        with open("config/secrets.py", "w") as f:
            f.write('"""Auto-generated empty secrets file."""\n')
            f.write('linkedin_email = ""\n')
            f.write('linkedin_password = ""\n')
            f.write('openai_api_key = ""\n')
            f.write('openai_model = "gpt-4"\n')

    return True


def show_menu():
    """Display the main menu."""
    print("\n  What would you like to do?\n")
    print("  1. 🚀 Start Auto Applying")
    print("  2. 📊 View Application Dashboard")
    print("  3. ⚙️  Edit Configuration")
    print("  4. ❓ Help")
    print("  5. 🚪 Exit")
    print()

    return input("  Enter your choice (1-5): ").strip()


def start_applying():
    """Start the LinkedIn bot."""
    from linkedin_bot import LinkedInBot
    from config import search

    print(f"\n  🔍 Search terms: {', '.join(search.search_terms)}")
    print(f"  📍 Location: {search.search_location or 'Any'}")
    print(f"  🎯 Max applications: {search.max_applications_per_session}")
    print(f"  🛡️ Easy Apply only: {search.easy_apply_only}")

    response = input("\n  Ready to start? (y/n): ").strip()
    if response.lower() != "y":
        print("  Cancelled.")
        return

    bot = LinkedInBot()
    bot.run()


def start_dashboard():
    """Start the web dashboard."""
    try:
        from dashboard.app import create_app
        app = create_app()
        print("\n  📊 Dashboard starting on http://localhost:5000")
        print("  Press Ctrl+C to stop\n")
        app.run(host="0.0.0.0", port=5000, debug=False)
    except ImportError:
        print("\n  ❌ Dashboard dependencies not installed.")
        print("  Run: pip install flask flask-cors")


def show_help():
    """Display help information."""
    print("""
  ╔══════════════════════════════════════════════════════════╗
  ║              LinkedIn AI Auto Job Applier                ║
  ╠══════════════════════════════════════════════════════════╣
  ║                                                          ║
  ║  SETUP:                                                  ║
  ║   1. Fill in config/personals.py with your details       ║
  ║   2. Fill in config/search.py with job preferences       ║
  ║   3. Fill in config/questions.py with Q&A answers        ║
  ║   4. Copy config/secrets.example.py → secrets.py         ║
  ║   5. Add your resume to the path in personals.py         ║
  ║                                                          ║
  ║  FIRST RUN:                                              ║
  ║   • Login to LinkedIn manually in the Chrome window      ║
  ║   • The bot will remember your session for next time     ║
  ║                                                          ║
  ║  AI FEATURES (Optional):                                 ║
  ║   • Add OpenAI API key in config/secrets.py              ║
  ║   • Enable AI resume customization in settings.py        ║
  ║   • Enable AI cover letter generation                    ║
  ║   • AI answers unknown application questions             ║
  ║                                                          ║
  ║  TIPS:                                                   ║
  ║   • Keep max_applications under 30 per session           ║
  ║   • LinkedIn caps Easy Apply at ~80-100/day              ║
  ║   • Solve CAPTCHAs manually — bot will wait              ║
  ║   • Use stealth_mode = True to avoid detection           ║
  ║                                                          ║
  ╚══════════════════════════════════════════════════════════╝
    """)


def main():
    """Main entry point."""
    print_banner()

    if not check_config():
        sys.exit(1)

    while True:
        choice = show_menu()

        if choice == "1":
            start_applying()
        elif choice == "2":
            start_dashboard()
        elif choice == "3":
            print("\n  📂 Config files are in the /config directory")
            print("  Edit them with any text editor.")
        elif choice == "4":
            show_help()
        elif choice == "5":
            print("\n  👋 Goodbye! Good luck with your job search!\n")
            break
        else:
            print("\n  ❌ Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()
