"""
LinkedIn AI Auto Job Applier — Main Bot Engine
Automates LinkedIn Easy Apply with AI-powered smart answers.

Author: Rayees Yousuf
GitHub: https://github.com/RayeesYousufGenAi
"""

import os
import sys
import json
import time
import random
import logging
from datetime import datetime

try:
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait, Select
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import (
        TimeoutException,
        NoSuchElementException,
        ElementClickInterceptedException,
        StaleElementReferenceException,
    )
except ImportError:
    print("❌ Missing dependencies. Run: pip install -r requirements.txt")
    sys.exit(1)

try:
    from config import personals, search, questions, settings
except ImportError:
    print("❌ Config files not found. Copy config/secrets.example.py → config/secrets.py")
    print("   Then fill in your details in config/ files.")
    sys.exit(1)


# ────────────────────────────────────────────────────────────────
# 📊 SESSION TRACKER
# ────────────────────────────────────────────────────────────────

class SessionTracker:
    """Tracks application statistics for the current session."""

    def __init__(self):
        self.applied = 0
        self.skipped = 0
        self.failed = 0
        self.errors = 0
        self.start_time = datetime.now()
        self.applied_jobs = []

    def record_applied(self, job_title: str, company: str, url: str):
        self.applied += 1
        self.applied_jobs.append({
            "title": job_title,
            "company": company,
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "status": "applied",
        })

    def record_skipped(self, reason: str = ""):
        self.skipped += 1

    def record_failed(self, reason: str = ""):
        self.failed += 1

    def get_summary(self) -> dict:
        elapsed = (datetime.now() - self.start_time).total_seconds()
        return {
            "applied": self.applied,
            "skipped": self.skipped,
            "failed": self.failed,
            "errors": self.errors,
            "duration_minutes": round(elapsed / 60, 1),
            "rate_per_hour": round((self.applied / elapsed) * 3600, 1) if elapsed > 0 else 0,
        }

    def save_to_file(self):
        """Save applied jobs to JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"applied_jobs_{timestamp}.json"

        data = {
            "session": self.get_summary(),
            "jobs": self.applied_jobs,
        }

        os.makedirs("logs", exist_ok=True)
        filepath = os.path.join("logs", filename)

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        return filepath


# ────────────────────────────────────────────────────────────────
# 🧠 SMART ANSWER ENGINE
# ────────────────────────────────────────────────────────────────

class SmartAnswerEngine:
    """Matches application questions to pre-configured answers using keyword matching."""

    def __init__(self):
        self.answers = questions.answers
        self.learned_answers = self._load_learned_answers()
        self.use_ai = getattr(questions, "use_ai_for_unknown_questions", False)

    def _load_learned_answers(self) -> dict:
        """Load previously saved answers from JSON."""
        filepath = "logs/learned_answers.json"
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return json.load(f)
        return {}

    def _save_learned_answer(self, question: str, answer: str):
        """Save a new question-answer pair for future use."""
        self.learned_answers[question.lower().strip()] = answer
        os.makedirs("logs", exist_ok=True)
        with open("logs/learned_answers.json", "w") as f:
            json.dump(self.learned_answers, f, indent=2)

    def get_answer(self, question_text: str) -> str | None:
        """Find the best answer for a given question using keyword matching."""
        question_lower = question_text.lower().strip()

        # 1. Check exact matches in learned answers
        if question_lower in self.learned_answers:
            return self.learned_answers[question_lower]

        # 2. Keyword matching against configured answers
        best_match = None
        best_match_length = 0

        for keyword, answer in self.answers.items():
            if keyword.lower() in question_lower:
                # Prefer longer keyword matches (more specific)
                if len(keyword) > best_match_length:
                    best_match = answer
                    best_match_length = len(keyword)

        if best_match:
            return str(best_match)

        # 3. AI fallback (if OpenAI key is configured)
        if self.use_ai:
            ai_answer = self._ask_ai(question_text)
            if ai_answer:
                self._save_learned_answer(question_text, ai_answer)
                return ai_answer

        return None

    def _ask_ai(self, question: str) -> str | None:
        """Use OpenAI to generate an answer for unknown questions."""
        try:
            from config import secrets
            if not getattr(secrets, "openai_api_key", ""):
                return None

            from openai import OpenAI
            client = OpenAI(api_key=secrets.openai_api_key)

            response = client.chat.completions.create(
                model=getattr(secrets, "openai_model", "gpt-4"),
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are filling out a job application form. "
                            "Give a short, professional answer to the following question. "
                            "Keep answers concise — typically 1-3 words or a short sentence. "
                            f"The applicant has {personals.years_of_experience} years of experience "
                            f"as a {personals.current_role}."
                        ),
                    },
                    {"role": "user", "content": question},
                ],
                max_tokens=100,
                temperature=0.3,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logging.warning(f"AI answer generation failed: {e}")
            return None


# ────────────────────────────────────────────────────────────────
# 🤖 LINKEDIN BOT
# ────────────────────────────────────────────────────────────────

class LinkedInBot:
    """Main LinkedIn Easy Apply automation bot."""

    LINKEDIN_URL = "https://www.linkedin.com"
    JOBS_URL = "https://www.linkedin.com/jobs/search/"

    def __init__(self):
        self.driver = None
        self.tracker = SessionTracker()
        self.answer_engine = SmartAnswerEngine()
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        """Configure session logging."""
        os.makedirs(settings.log_directory, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        log_file = os.path.join(settings.log_directory, f"session_{timestamp}.log")

        logger = logging.getLogger("LinkedInBot")
        logger.setLevel(getattr(logging, settings.log_level, logging.INFO))

        # File handler
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(fh)

        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(ch)

        return logger

    def _init_driver(self):
        """Initialize Chrome browser with stealth settings."""
        options = uc.ChromeOptions()

        # Persistent profile
        profile_path = os.path.abspath(settings.chrome_profile_path)
        os.makedirs(profile_path, exist_ok=True)
        options.add_argument(f"--user-data-dir={profile_path}")

        # Anti-detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")

        if settings.run_in_background:
            options.add_argument("--headless=new")

        self.driver = uc.Chrome(options=options)
        self.driver.set_page_load_timeout(settings.page_load_timeout)
        self.logger.info("✅ Browser initialized successfully")

    def _random_delay(self, min_s=None, max_s=None):
        """Add human-like random delay."""
        min_s = min_s or settings.min_click_delay
        max_s = max_s or settings.max_click_delay
        delay = random.uniform(min_s, max_s)
        time.sleep(delay)

    def _human_type(self, element, text: str):
        """Type text with human-like delays between keystrokes."""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(
                settings.min_typing_delay,
                settings.max_typing_delay,
            ))

    def _wait_for_element(self, by, value, timeout=None):
        """Wait for an element to be clickable."""
        timeout = timeout or settings.element_wait_timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            return None

    def _login(self):
        """Login to LinkedIn (uses saved session or credentials)."""
        self.driver.get(self.LINKEDIN_URL)
        self._random_delay(2, 4)

        # Check if already logged in
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".feed-identity-module")
            self.logger.info("✅ Already logged in via saved session")
            return True
        except NoSuchElementException:
            pass

        # Try credential login
        try:
            from config import secrets
            email = getattr(secrets, "linkedin_email", "")
            password = getattr(secrets, "linkedin_password", "")

            if email and password:
                self.logger.info("🔐 Logging in with credentials...")
                self.driver.get(f"{self.LINKEDIN_URL}/login")
                self._random_delay(1, 3)

                email_field = self._wait_for_element(By.ID, "username")
                if email_field:
                    self._human_type(email_field, email)

                password_field = self._wait_for_element(By.ID, "password")
                if password_field:
                    self._human_type(password_field, password)

                submit_btn = self._wait_for_element(
                    By.CSS_SELECTOR, "button[type='submit']"
                )
                if submit_btn:
                    submit_btn.click()

                self._random_delay(3, 5)
                self.logger.info("✅ Login submitted")
                return True
            else:
                self.logger.info("⚠️ No credentials provided — please login manually")
                self.logger.info("   The bot will wait 60 seconds for manual login...")
                time.sleep(60)
                return True

        except Exception as e:
            self.logger.error(f"❌ Login failed: {e}")
            return False

    def _build_search_url(self, keyword: str) -> str:
        """Build LinkedIn job search URL with filters."""
        params = [f"keywords={keyword.replace(' ', '%20')}"]

        if search.search_location:
            params.append(f"location={search.search_location.replace(' ', '%20')}")

        if search.easy_apply_only:
            params.append("f_AL=true")  # Easy Apply filter

        # Date posted
        date_map = {
            "Past 24 hours": "r86400",
            "Past week": "r604800",
            "Past month": "r2592000",
        }
        if search.date_posted in date_map:
            params.append(f"f_TPR={date_map[search.date_posted]}")

        return f"{self.JOBS_URL}?{'&'.join(params)}"

    def _get_job_cards(self) -> list:
        """Get all job listing cards from the current page."""
        try:
            self._random_delay(1, 2)
            cards = self.driver.find_elements(
                By.CSS_SELECTOR,
                ".job-card-container, .jobs-search-results__list-item"
            )
            return cards
        except Exception:
            return []

    def _extract_job_info(self, card) -> dict:
        """Extract job title, company, and URL from a job card."""
        info = {"title": "", "company": "", "url": "", "location": ""}
        try:
            title_el = card.find_element(By.CSS_SELECTOR, ".job-card-list__title, a.job-card-container__link")
            info["title"] = title_el.text.strip()
            info["url"] = title_el.get_attribute("href") or ""

            company_el = card.find_element(By.CSS_SELECTOR, ".job-card-container__primary-description, .artdeco-entity-lockup__subtitle")
            info["company"] = company_el.text.strip()

            location_el = card.find_element(By.CSS_SELECTOR, ".job-card-container__metadata-wrapper, .artdeco-entity-lockup__caption")
            info["location"] = location_el.text.strip()
        except NoSuchElementException:
            pass
        return info

    def _should_skip_job(self, job_info: dict) -> str | None:
        """Check if a job should be skipped. Returns skip reason or None."""
        title = job_info.get("title", "").lower()
        company = job_info.get("company", "").lower()

        # Blacklisted companies
        for bc in search.blacklisted_companies:
            if bc.lower() in company:
                return f"Blacklisted company: {bc}"

        # Skip keywords in title
        for kw in search.skip_keywords_in_title:
            if kw.lower() in title:
                return f"Skip keyword in title: {kw}"

        return None

    def _fill_form_field(self, field, answer: str):
        """Fill a form field with the given answer."""
        try:
            tag = field.tag_name.lower()

            if tag == "input":
                input_type = field.get_attribute("type") or "text"

                if input_type in ("text", "tel", "email", "number", "url"):
                    field.clear()
                    self._human_type(field, answer)

                elif input_type == "radio":
                    field.click()

                elif input_type == "checkbox":
                    if not field.is_selected():
                        field.click()

            elif tag == "select":
                select = Select(field)
                # Try exact match first, then partial
                for option in select.options:
                    if answer.lower() in option.text.lower():
                        select.select_by_visible_text(option.text)
                        break

            elif tag == "textarea":
                field.clear()
                self._human_type(field, answer)

            self._random_delay(0.3, 0.8)

        except Exception as e:
            self.logger.warning(f"⚠️ Could not fill field: {e}")

    def _handle_easy_apply_modal(self) -> bool:
        """Handle the multi-step Easy Apply modal dialog."""
        max_pages = 10  # Safety limit

        for page in range(max_pages):
            self._random_delay(1, 2)

            # Find all form fields on current page
            try:
                form_groups = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    ".jobs-easy-apply-form-section__grouping"
                )

                for group in form_groups:
                    try:
                        # Get question text
                        label = group.find_element(By.CSS_SELECTOR, "label, legend, span").text
                        if not label:
                            continue

                        # Get answer from engine
                        answer = self.answer_engine.get_answer(label)

                        if answer:
                            # Find fillable field
                            fields = group.find_elements(By.CSS_SELECTOR, "input, select, textarea")
                            for field in fields:
                                if field.is_displayed():
                                    self._fill_form_field(field, answer)
                                    break

                            self.logger.debug(f"   ✅ Answered: '{label[:50]}' → '{answer}'")
                        else:
                            self.logger.warning(f"   ⚠️ No answer for: '{label[:80]}'")

                    except NoSuchElementException:
                        continue

                # Handle resume upload if present
                try:
                    upload_input = self.driver.find_element(
                        By.CSS_SELECTOR, "input[type='file']"
                    )
                    resume_path = os.path.abspath(personals.default_resume_path)
                    if os.path.exists(resume_path):
                        upload_input.send_keys(resume_path)
                        self.logger.info("   📄 Resume uploaded")
                        self._random_delay(1, 2)
                except NoSuchElementException:
                    pass

            except Exception as e:
                self.logger.warning(f"⚠️ Error processing form page: {e}")

            # Check for Submit button
            try:
                submit_btn = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "button[aria-label*='Submit'], button[data-control-name*='submit']"
                )
                if submit_btn.is_displayed():
                    if getattr(questions, "pause_before_submit", False):
                        self.logger.info("⏸️ Paused before submit — review in browser")
                        input("Press Enter to continue...")

                    submit_btn.click()
                    self._random_delay(1, 2)
                    self.logger.info("   ✅ Application submitted!")
                    return True
            except NoSuchElementException:
                pass

            # Click Next / Continue / Review
            try:
                next_btn = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "button[aria-label*='Continue'], button[aria-label*='Next'], button[aria-label*='Review']"
                )
                if next_btn.is_displayed():
                    next_btn.click()
                    self._random_delay(1, 2)
                    continue
            except NoSuchElementException:
                break

        return False

    def _apply_to_job(self, job_info: dict) -> bool:
        """Apply to a single job using Easy Apply."""
        try:
            # Click Easy Apply button
            easy_apply_btn = self._wait_for_element(
                By.CSS_SELECTOR,
                ".jobs-apply-button, button[aria-label*='Easy Apply']",
                timeout=5,
            )

            if not easy_apply_btn:
                self.logger.info(f"   ⏭️ No Easy Apply button found")
                return False

            easy_apply_btn.click()
            self._random_delay(1, 3)

            # Handle the modal
            success = self._handle_easy_apply_modal()

            if success:
                self.tracker.record_applied(
                    job_info["title"],
                    job_info["company"],
                    job_info["url"],
                )
                self.logger.info(
                    f"✅ Applied: \"{job_info['title']}\" at {job_info['company']}"
                )

                # Close any post-apply dialogs
                try:
                    dismiss_btn = self.driver.find_element(
                        By.CSS_SELECTOR, "button[aria-label*='Dismiss']"
                    )
                    dismiss_btn.click()
                except NoSuchElementException:
                    pass

            return success

        except Exception as e:
            self.logger.error(f"❌ Error applying to {job_info.get('title', 'Unknown')}: {e}")
            self.tracker.record_failed(str(e))
            return False

    def _process_search_results(self, keyword: str):
        """Process all job listings for a search keyword."""
        url = self._build_search_url(keyword)
        self.driver.get(url)
        self._random_delay(3, 5)

        self.logger.info(f"\n🔍 Searching: \"{keyword}\"")
        self.logger.info(f"   URL: {url}")

        page = 1
        while self.tracker.applied < search.max_applications_per_session:
            self.logger.info(f"\n📄 Page {page}")
            cards = self._get_job_cards()

            if not cards:
                self.logger.info("   No more job cards found")
                break

            for card in cards:
                if self.tracker.applied >= search.max_applications_per_session:
                    self.logger.info("🛑 Application limit reached!")
                    return

                job_info = self._extract_job_info(card)
                if not job_info["title"]:
                    continue

                # Check skip rules
                skip_reason = self._should_skip_job(job_info)
                if skip_reason:
                    self.logger.info(f"   ⏭️ Skipped: {job_info['title']} — {skip_reason}")
                    self.tracker.record_skipped(skip_reason)
                    continue

                self.logger.info(f"\n   📋 Processing: \"{job_info['title']}\" at {job_info['company']}")

                # Click on job card
                try:
                    card.click()
                    self._random_delay(1, 3)
                except Exception:
                    continue

                # Apply
                self._apply_to_job(job_info)
                self._random_delay(
                    settings.min_application_delay,
                    settings.max_application_delay,
                )

            # Navigate to next page
            page += 1
            try:
                next_page = self.driver.find_element(
                    By.CSS_SELECTOR,
                    f"button[aria-label='Page {page}'], li[data-test-pagination-page-btn='{page}'] button"
                )
                next_page.click()
                self._random_delay(2, 4)
            except NoSuchElementException:
                self.logger.info("   No more pages")
                break

    def run(self):
        """Main execution method — runs the full automation pipeline."""
        try:
            self.logger.info("=" * 60)
            self.logger.info("  🤖 LinkedIn AI Auto Job Applier")
            self.logger.info(f"  📅 Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.logger.info("=" * 60)

            # Initialize browser
            self._init_driver()

            # Login
            if not self._login():
                self.logger.error("❌ Login failed. Exiting.")
                return

            # Process each search term
            keywords = list(search.search_terms)
            if search.randomize_search_order:
                random.shuffle(keywords)

            for keyword in keywords:
                if self.tracker.applied >= search.max_applications_per_session:
                    break
                self._process_search_results(keyword)

            # Session complete
            summary = self.tracker.get_summary()
            self.logger.info("\n" + "=" * 60)
            self.logger.info("  📊 SESSION SUMMARY")
            self.logger.info("=" * 60)
            self.logger.info(f"  ✅ Applied:   {summary['applied']}")
            self.logger.info(f"  ⏭️ Skipped:   {summary['skipped']}")
            self.logger.info(f"  ❌ Failed:    {summary['failed']}")
            self.logger.info(f"  ⏱️ Duration:  {summary['duration_minutes']} minutes")
            self.logger.info(f"  📈 Rate:      {summary['rate_per_hour']} apps/hour")
            self.logger.info("=" * 60)

            # Save results
            if settings.auto_save_applied_jobs:
                filepath = self.tracker.save_to_file()
                self.logger.info(f"💾 Results saved to: {filepath}")

        except KeyboardInterrupt:
            self.logger.info("\n⛔ Session interrupted by user")
        except Exception as e:
            self.logger.error(f"❌ Fatal error: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("🔒 Browser closed")
