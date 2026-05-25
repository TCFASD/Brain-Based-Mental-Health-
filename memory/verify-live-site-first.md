---
name: verify-live-site-first
description: Before making changes to the mockup, or before describing the current website state, always re-read the live site files (index.html, about-us.html, etc. at repo root) to confirm current content. The live site evolves and the version I'm holding may be stale.
metadata:
  type: feedback
---

When working on the Brain-Based Mental Health website, the live site files at the repo root (index.html, about-us.html, professionals.html, caregivers.html, self-advocates.html, organizations.html, resources.html) are continuously edited by the user and other contributors. The version of these files I have in context from earlier in a session may be out of date by the time I make follow-up changes.

**Why:** Twice in one session I made changes based on a stale view of the website — once applying redundant edits to the mockup that were already done on the live site, once writing the wrong hero title structure. The user had to correct me both times.

**How to apply:** Before applying any change to a mockup that's supposed to mirror the live site, re-read the corresponding live HTML file. Before describing what's currently on the website to the user, re-read the file. Do not rely on memory of earlier reads when the user implies things have changed ("we made changes," "the title changed," "you are not using the most up to date").

Mockup pages live in `Mock-up Website/Up to Date Mock pages/`. Corresponding live pages are at the repo root with names like `index.html`, `about-us.html`, etc.
