"""Convert any Markdown file in the repo to Word using the shared converter.

Usage: py scripts/md_to_docx.py <path-to-markdown>

Example: py scripts/md_to_docx.py "Group Feedback/Working-Group-Meeting-Agenda.md"
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import generate_feedback_summary_docx as g

if len(sys.argv) < 2:
    print("Usage: py scripts/md_to_docx.py <path-to-markdown>")
    sys.exit(1)

md_path = Path(sys.argv[1])
if not md_path.is_absolute():
    md_path = ROOT / md_path

if not md_path.exists():
    print(f"File not found: {md_path}")
    sys.exit(1)

g.MD = md_path
g.OUT = md_path.with_suffix(".docx")
g.main()
