"""
Applied Jobs Dashboard — View your application history in a web browser.
Run: python -m dashboard.app
Then open: http://localhost:5000
"""

import os
import json
import glob
from flask import Flask, render_template, jsonify
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/sessions")
    def get_sessions():
        """List all session files."""
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        files = sorted(glob.glob(os.path.join(log_dir, "applied_jobs_*.json")), reverse=True)

        sessions = []
        for f in files:
            try:
                with open(f, "r") as fh:
                    data = json.load(fh)
                    sessions.append({
                        "filename": os.path.basename(f),
                        "summary": data.get("session", {}),
                        "job_count": len(data.get("jobs", [])),
                    })
            except (json.JSONDecodeError, KeyError):
                continue

        return jsonify(sessions)

    @app.route("/api/sessions/<filename>")
    def get_session_detail(filename):
        """Get details for a specific session."""
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        filepath = os.path.join(log_dir, filename)

        if not os.path.exists(filepath):
            return jsonify({"error": "Session not found"}), 404

        with open(filepath, "r") as f:
            data = json.load(f)

        return jsonify(data)

    @app.route("/api/stats")
    def get_stats():
        """Get aggregated stats across all sessions."""
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        files = glob.glob(os.path.join(log_dir, "applied_jobs_*.json"))

        total_applied = 0
        total_skipped = 0
        total_failed = 0
        all_companies = set()
        all_jobs = []

        for f in files:
            try:
                with open(f, "r") as fh:
                    data = json.load(fh)
                    session = data.get("session", {})
                    total_applied += session.get("applied", 0)
                    total_skipped += session.get("skipped", 0)
                    total_failed += session.get("failed", 0)

                    for job in data.get("jobs", []):
                        all_companies.add(job.get("company", ""))
                        all_jobs.append(job)
            except (json.JSONDecodeError, KeyError):
                continue

        return jsonify({
            "total_applied": total_applied,
            "total_skipped": total_skipped,
            "total_failed": total_failed,
            "total_sessions": len(files),
            "unique_companies": len(all_companies),
            "recent_jobs": sorted(all_jobs, key=lambda x: x.get("timestamp", ""), reverse=True)[:20],
        })

    return app


if __name__ == "__main__":
    app = create_app()
    print("\n📊 Dashboard running at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
