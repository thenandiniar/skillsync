# SkillSync

A beginner-friendly Flask project that:
- Uploads a resume PDF
- Extracts text using **pdfplumber**
- Matches extracted resume skills against job description skills
- Shows match percentage, matching skills, and missing skills

## Setup

1) Create a virtual environment (recommended)

```bash
python -m venv venv
```

2) Activate it

Windows (PowerShell):
```bash
venv\\Scripts\\Activate.ps1
```

3) Install dependencies

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Open your browser at:
- http://127.0.0.1:5000

## Notes

- This demo uses a small fixed skill database.
- Skill matching is done using simple text substring matching.
- For best results, upload a resume PDF with selectable text (not scanned images).

