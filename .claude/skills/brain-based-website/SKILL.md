---
name: brain-based-website
description: Context and workflow guide for the Brain-Based Mental Health website project. Use when editing mockup pages, building Google Sites pages via Playwright, reviewing content, or discussing site structure. Triggers on "website", "mockup", "page", "Google Sites", "draft site", "combined structure".
---

# Brain-Based Mental Health Website — Project Skill

## Project Overview

This project merges **two existing Google Sites** into one unified website for **Brain-Based Mental Health** (part of the FASD United Mental Health Work Group):

1. **Brain-Based Community (BBC)** — 16 pages, comprehensive professional content (`raw-html/`)
2. **Florida Center (FC)** — 8 pages, simplified visual versions with cartoon brain graphics (`florida-center/raw-html/`)

**Result:** A single 16-page site using BBC as the base, integrating FC's unique visual assets and plain-language handouts, eliminating duplication.

**Target platform:** Google Sites (not custom code — all implementation must work within Google Sites constraints).

## Key Files & Where to Find Content

| What you need | Where to look |
|---|---|
| Authoritative site blueprint | `COMBINED-STRUCTURE.md` (root) |
| Overlap analysis | `SITE-COMPARISON.md` (root) |
| Current BBC page index | `SITE-MAP.md` (root) |
| **Up-to-date mockup pages** | `Mock-up Website/Up to Date Mock pages/` |
| Older mockup drafts | `Mock-up Website/` (root of that folder) |
| Original BBC HTML | `raw-html/` |
| Original FC HTML | `florida-center/raw-html/` |
| FC screenshots | `florida-center/screenshots/` |
| Approved images | `images/approved/` |
| Candidate images | `images/candidates/` |
| PDF handouts | `handouts/` |
| Site screenshots | `screenshots/` |

**Always read the mockup HTML file before editing a Google Sites page** — it contains the exact text to use.

## Site Structure (16 Pages)

**Top-level navigation:** Home | About Us | Professionals > | Caregivers | Self-Advocates | Organizations | Resources >

### Page Sources

| Page | Primary Source | FC Assets to Integrate |
|---|---|---|
| Home | BBC + new mockup | — |
| About Us | BBC + new mockup | — |
| Professionals | BBC + new mockup | — |
| → Foundational Knowledge | BBC | FC brain graphic, webinar |
| → Brain-Based Fundamentals | BBC | FC brain graphic, webinar |
| → Assessment | BBC | FC brain graphic, webinar, plain-language handout |
| → Treatment Planning | BBC | FC brain graphic, webinar, plain-language handout |
| → Therapeutic Strategies | BBC | FC brain graphic, webinar, plain-language handout |
| → Professional Community | BBC | FC brain graphic |
| Caregivers | BBC | — |
| Self-Advocates | BBC | — |
| Organizations | BBC | — |
| Resources | BBC | — |
| → Self-Assessment | BBC | — |
| → Brain-Based Competencies | BBC | — |

## Design System

### Typography (Accessibility-First)
- **Headings:** Lexend (designed for reading proficiency / dyslexia support)
- **Body:** Open Sans (high legibility, open apertures)
- Body size: 17px, Line height: 1.7
- All text left-aligned, short paragraphs, generous whitespace

### Color Palette
- **Primary:** `#1a3a6b` (dark navy) — nav, main headings
- **Secondary:** `#2c5aa0` (medium blue) — accents, buttons
- **Teal/Green:** `#0e8a6e` — Caregivers audience accent
- **Purple:** `#7c3aed` — Self-Advocates audience accent
- **Background:** `#fff` (white), `#f7f9fc` (light blue sections)
- **Text:** `#222` headings, `#333`–`#444` body

### Layout Patterns
- Card-based layouts with shadows and hover effects
- Gradient hero sections
- Alternating section background colors (Style 1/2/3 in Google Sites)
- Responsive 3-column grid for audience cards

### Google Sites Theme
- **Theme:** Diplomat
- **Color:** Dark Blue
- **Font style:** Light

## Content Rules

1. **Use EXACT text from mockup HTML files.** Do not paraphrase or rewrite.
2. **For handouts, preserve original TFC (Florida Center) writing** — do not modify.
3. **Do NOT use personal Google Drive photos.** Only use `images/approved/` or royalty-free sources.
4. **Stay on the draft site only.** Do not navigate to or modify other websites.
5. **"Look prettier" = themes, fonts, section colors, layout** — not adding more text.

## Audiences

The site serves three distinct groups — content and tone differ per audience:

1. **Professionals/Clinicians** — Seeking brain-based practice training (primary audience, most content)
2. **Caregivers** — Family members supporting people with neurodevelopmental differences
3. **Self-Advocates** — Individuals with FASD, neurodevelopmental conditions, or acquired brain differences

## Workflow: Editing Google Sites via Playwright

For detailed Playwright patterns (text entry, themes, clicking workarounds, iframes), see `references/google-sites-patterns.md`.

### General Workflow
1. Read the target mockup HTML file for exact content
2. Navigate to the draft Google Sites editor
3. Create/edit the page using Playwright MCP tools
4. Apply theme styling (Diplomat, Dark Blue, Light)
5. Use alternating section backgrounds for visual rhythm
6. Take screenshots for verification

## Key Context

- **Brain-Based Pathway** = 6-stage professional development model (Foundational Knowledge → Fundamentals → Assessment → Treatment Planning → Therapeutic Strategies → Community)
- **Two practice levels:** "Informed" (foundational) vs "Responsive" (advanced)
- **FASD** = Fetal Alcohol Spectrum Disorder — major focus of this initiative
- The 50-item **Self-Assessment Tool** and **10-Competency Framework** are key resources
- FC's unique assets worth preserving: cartoon brain stage graphics, plain-language handout versions, poster PDF
