"""Convert Combined-Feedback-By-Section.md to a Word document.

Reuses the markdown-to-docx logic in generate_feedback_summary_docx.py
but points at the Combined-Feedback file instead.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import generate_feedback_summary_docx as g

g.MD = ROOT / "Group Feedback" / "Combined-Feedback-By-Section.md"
g.OUT = ROOT / "Group Feedback" / "Combined-Feedback-By-Section.docx"

if __name__ == "__main__":
    g.main()
