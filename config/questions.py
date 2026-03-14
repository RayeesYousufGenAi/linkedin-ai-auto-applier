"""
Config: Application Q&A — Answers for screening questions
The bot uses keyword matching to find the right answer for each question.
"""

# ────────────────────────────────────────────────────────────────
# ❓ QUESTION-ANSWER MAPPINGS
# ────────────────────────────────────────────────────────────────
# Format: "keyword_in_question": "your_answer"
# The bot scans each question for these keywords and fills the answer.

answers = {
    # Work Authorization
    "authorized": "Yes",
    "work authorization": "Yes",
    "legally authorized": "Yes",
    "eligible to work": "Yes",
    "right to work": "Yes",
    "us citizen": "Yes",
    "citizenship": "Yes, I am authorized to work",

    # Visa & Sponsorship
    "visa": "No",
    "sponsorship": "No",
    "require sponsorship": "No",
    "need sponsorship": "No",
    "immigration sponsorship": "No",
    "h1b": "No",
    "h-1b": "No",

    # Relocation
    "relocate": "Yes",
    "relocation": "Yes",
    "willing to relocate": "Yes",
    "open to relocation": "Yes",

    # Experience
    "years of experience": "3",
    "total experience": "3",
    "how many years": "3",
    "experience in": "3",
    "relevant experience": "3",

    # Education
    "bachelor": "Yes",
    "master": "No",
    "phd": "No",
    "highest degree": "Bachelor's Degree",
    "education level": "Bachelor's Degree",
    "gpa": "3.8",

    # Salary
    "salary": "80000",
    "compensation": "80000",
    "expected salary": "80000",
    "desired salary": "80000",
    "salary expectation": "80000",
    "pay expectation": "80000",
    "minimum salary": "70000",
    "annual salary": "80000",

    # Availability
    "start date": "Immediately",
    "when can you start": "Immediately",
    "available to start": "Immediately",
    "earliest start": "Within 2 weeks",
    "notice period": "15 days",
    "availability": "Immediately",

    # Remote / On-site
    "remote": "Yes",
    "work remotely": "Yes",
    "hybrid": "Yes",
    "on-site": "Yes",
    "office": "Yes",
    "commute": "Yes",
    "work from home": "Yes",

    # Travel
    "travel": "Yes, up to 25%",
    "willing to travel": "Yes",
    "business travel": "Yes",
    "travel requirement": "Yes, willing to travel",

    # Skills (customize based on your skills)
    "python": "Yes",
    "javascript": "Yes",
    "java": "No",
    "sql": "Yes",
    "aws": "Yes",
    "docker": "Yes",
    "kubernetes": "Yes",
    "react": "Yes",
    "machine learning": "Yes",
    "deep learning": "Yes",
    "nlp": "Yes",
    "ai": "Yes",
    "git": "Yes",
    "agile": "Yes",
    "scrum": "Yes",

    # Background
    "background check": "Yes",
    "drug test": "Yes",
    "criminal record": "No",
    "felony": "No",
    "misdemeanor": "No",

    # Personal
    "gender": "Decline to answer",
    "race": "Decline to answer",
    "ethnicity": "Decline to answer",
    "veteran": "No",
    "disability": "Decline to answer",
    "lgbtq": "Decline to answer",

    # LinkedIn-specific
    "how did you hear": "LinkedIn",
    "referral": "No",
    "how did you find": "LinkedIn Job Search",
    "source": "LinkedIn",

    # Cover Letter
    "cover letter": "I am excited to apply for this role. My experience aligns well with the requirements.",
    "additional information": "Thank you for considering my application.",
    "anything else": "I look forward to the opportunity to contribute to your team.",

    # Misc
    "acknowledge": "Yes",
    "agree": "Yes",
    "confirm": "Yes",
    "consent": "Yes",
    "certify": "Yes",
    "attest": "Yes",
    "18 years": "Yes",
    "legal age": "Yes",
}

# ────────────────────────────────────────────────────────────────
# 🤖 AI FALLBACK SETTINGS
# ────────────────────────────────────────────────────────────────

# If the bot can't find an answer using keyword matching,
# should it use OpenAI to generate an answer?
use_ai_for_unknown_questions = True

# Should the bot pause before submitting each application?
# Useful for reviewing answers before they're sent
pause_before_submit = False

# Should the bot pause if it encounters an unknown question?
pause_on_unknown_question = False

# Save new question-answer pairs to a JSON file for future use
save_new_answers = True
