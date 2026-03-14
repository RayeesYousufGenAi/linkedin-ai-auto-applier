"""
Config: Search Preferences & Job Filters
Configure which jobs the bot should apply to or skip.
"""

# ────────────────────────────────────────────────────────────────
# 🔍 SEARCH TERMS
# ────────────────────────────────────────────────────────────────

# Job titles/keywords to search for (bot will search each one)
search_terms = [
    "Software Engineer",
    "AI Engineer",
    "Data Scientist",
    "Machine Learning Engineer",
]

# Do you want to randomize the search order for search_terms?
randomize_search_order = True

# Search location — fills "City, state, or zip code" search box
# Leave empty ("") to not fill the location filter
search_location = "United States"

# ────────────────────────────────────────────────────────────────
# 🏷️ JOB FILTERS
# ────────────────────────────────────────────────────────────────

# Only apply to Easy Apply jobs?
easy_apply_only = True

# Date posted filter: "Any time", "Past month", "Past week", "Past 24 hours"
date_posted = "Past week"

# Experience level filter (select all that apply)
# Options: "Internship", "Entry level", "Associate", "Mid-Senior level", "Director", "Executive"
experience_level = ["Entry level", "Associate", "Mid-Senior level"]

# Job type filter
# Options: "Full-time", "Part-time", "Contract", "Temporary", "Internship", "Volunteer"
job_type = ["Full-time"]

# Remote filter
# Options: "On-site", "Remote", "Hybrid"
remote_filter = ["Remote", "Hybrid"]

# ────────────────────────────────────────────────────────────────
# ⚙️ APPLICATION LIMITS
# ────────────────────────────────────────────────────────────────

# Maximum applications per session (LinkedIn caps at ~80-100/day)
max_applications_per_session = 30

# Skip jobs requiring more experience than this (set -1 to apply to all)
current_experience = 3

# ────────────────────────────────────────────────────────────────
# 🚫 BLACKLIST / SKIP RULES
# ────────────────────────────────────────────────────────────────

# Skip jobs from these companies
blacklisted_companies = [
    # "Company Name",
]

# Skip jobs containing these words in title
skip_keywords_in_title = [
    "Senior Director",
    "VP",
    "Principal",
    "Staff Engineer",
]

# Skip jobs containing these words in description
bad_words_in_description = [
    "10+ years required",
    "security clearance required",
]

# ────────────────────────────────────────────────────────────────
# ✅ PREFERRED COMPANIES (Optional)
# ────────────────────────────────────────────────────────────────

# Prioritize applications to these companies
preferred_companies = [
    # "Google",
    # "Microsoft",
    # "OpenAI",
]
