from flask import Flask, render_template, request
import pdfplumber
import os
import re

app = Flask(__name__)

# Ensure uploads folder exists
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# A small curated skills database (as requested)
SKILL_DB = [
    "python",
    "java",
    "c++",
    "sql",
    "machine learning",
    "deep learning",
    "html",
    "css",
    "javascript",
    "react",
    "flask",
    "django",
    "power bi",
    "excel",
    "git",
    "tensorflow",
    "pandas",
]

# Build a mapping to display nicer capitalization
DISPLAY_SKILLS = {
    "python": "Python",
    "java": "Java",
    "c++": "C++",
    "sql": "SQL",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "html": "HTML",
    "css": "CSS",
    "javascript": "JavaScript",
    "react": "React",
    "flask": "Flask",
    "django": "Django",
    "power bi": "Power BI",
    "excel": "Excel",
    "git": "Git",
    "tensorflow": "TensorFlow",
    "pandas": "Pandas",
}


def normalize_text(text: str) -> str:
    """Normalize text to make skill matching easier."""
    text = text.lower()

    # Convert common variants to something consistent
    text = text.replace("c#", "c++")  # (kept harmless; not required) 
    text = text.replace("machine-learning", "machine learning")
    text = text.replace("deep-learning", "deep learning")
    text = text.replace("powerbi", "power bi")
    text = text.replace("js", "javascript")

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_pdf_text(pdf_path: str) -> str:
    """Extract text from a PDF using pdfplumber."""
    extracted = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted.append(page.extract_text() or "")
    return "\n".join(extracted)


def extract_skills(text: str) -> set[str]:
    """Find which skills from SKILL_DB appear in the given text."""
    text_norm = normalize_text(text)

    found = set()
    for skill in SKILL_DB:
        # Simple substring match; beginner-friendly and fast for this project
        if skill in text_norm:
            found.add(skill)

    return found


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    # Read inputs
    job_description = request.form.get("job_description", "")
    resume_file = request.files.get("resume")

    if not resume_file or resume_file.filename == "":
        return render_template(
            "index.html",
            error="Please upload a resume PDF.",
        )

    if not job_description.strip():
        return render_template(
            "index.html",
            error="Please paste a job description.",
        )

    # Save uploaded file
    filename = resume_file.filename
    safe_name = re.sub(r"[^a-zA-Z0-9_.-]", "_", filename)
    save_path = os.path.join(UPLOAD_FOLDER, safe_name)
    resume_file.save(save_path)

    # Extract resume text
    try:
        resume_text = extract_pdf_text(save_path)
    except Exception:
        return render_template(
            "index.html",
            error="Could not extract text from that PDF. Please upload a valid resume PDF.",
        )

    # Extract skills
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    # Compare skills
    matching = resume_skills.intersection(job_skills)
    missing = job_skills.difference(resume_skills)

    # Match percentage based on job-required skills
    if len(job_skills) == 0:
        match_percentage = 0
    else:
        match_percentage = round((len(matching) / len(job_skills)) * 100)

    # Convert to display forms (keep consistent ordering with SKILL_DB)
    def to_display(skills_set: set[str]) -> list[str]:
        ordered = [s for s in SKILL_DB if s in skills_set]
        return [DISPLAY_SKILLS.get(s, s.title()) for s in ordered]

    return render_template(
        "index.html",
        match_percentage=match_percentage,
        matching_skills=to_display(matching),
        missing_skills=to_display(missing),
        job_skills_count=len(job_skills),
        error=None,
    )


if __name__ == "__main__":
    # Start in debug mode as requested
    app.run(debug=True)

