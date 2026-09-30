# The Taj Mahal Mystery — Implementation Plan

## Project Overview

A complete 30-page printable children's history adventure book (8.5 × 11 in portrait) for ages 8–12. Combines historical education about the Taj Mahal with a fictional mystery/adventure framework. The child plays the role of an "explorer" solving a mystery by learning real history.

---

## Staged Execution Plan

### STAGE A — Research & Fact Sheet
Research authoritative sources (UNESCO, Archaeological Survey of India, scholarly references) and produce a verified historical fact sheet and source list. All historical claims in the book map back to this document.

### STAGE B — 30-Page Manuscript
Write the full text content for all 30 pages — story, educational content, activities, and instructions — validated against the fact sheet.

### STAGE C — Visual Design System
Define: color palette, typography, character design, icon system, blueprint piece system, page layout template, and illustration style guide.

### STAGE D — Page Production (Batched)
Generate all 30 pages in batches of 5–6, applying QA checks between batches.

### STAGE E — Final QA & Export
Full consistency check across all 30 pages, then export PDF + supporting documents.

---

## Deliverables

| # | Artifact | Description |
|---|----------|-------------|
| 1 | `fact_sheet.md` | Verified historical facts with sources |
| 2 | `source_list.md` | Bibliography of authoritative sources |
| 3 | `manuscript.md` | Full 30-page text/activity script |
| 4 | `style_guide.md` | Visual design system (colors, fonts, layout) |
| 5 | `character_reference.md` | Explorer character design spec |
| 6 | `answer_key.md` | Internal reference answers for all activities |
| 7 | `qa_report.md` | Final QA checklist results |
| 8 | `pages/page_01.png … page_30.png` | Individual high-res page images |
| 9 | `tajmahal_mystery.pdf` | Final 30-page printable PDF |

---

## Page Map

| Page | Title | Level | Blueprint Piece |
|------|-------|-------|-----------------|
| 1 | The Mysterious Blueprint | Observer | — (intro) |
| 2 | Welcome to Agra | Observer | Piece #1 – Agra |
| 3 | Meet Shah Jahan | Observer | Piece #2 – People |
| 4 | Why Was the Taj Mahal Built? | Observer | — |
| 5 | The Architect's Table | Explorer | — |
| 6 | Rebuild the Symmetry | Explorer | Piece #3 – Architecture |
| 7 | The Four Minarets | Explorer | — |
| 8 | The Dome Challenge | Explorer | — |
| 9 | The Marble Mission | Explorer | — |
| 10 | Become a Stone-Inlay Artist | Explorer | Piece #4 – Art & Craft |
| 11 | The Calligrapher's Secret | Investigator | — |
| 12 | Who Built It? | Investigator | — |
| 13 | The Materials Journey | Investigator | — |
| 14 | The Garden Mystery | Investigator | — |
| 15 | Become the Water Engineer | Investigator | Piece #5 – Gardens & Engineering |
| 16 | The Reflection Puzzle | Investigator | — |
| 17 | The Taj Mahal from Above | Investigator | — |
| 18 | The Complex Detective | Investigator | — |
| 19 | Geometry Hunt | Historian | — |
| 20 | The Inscription Investigation | Historian | — |
| 21 | Myth or History? | Historian | — |
| 22 | The Historian's Evidence Box | Historian | Piece #6 – Evidence |
| 23 | The Damaged Blueprint | Creator | — (all 6 assembled) |
| 24 | The Final Architect's Challenge | Creator | — |
| 25 | Design Your Own Mughal-Inspired Garden | Creator | — |
| 26 | A Day in 17th-Century Agra | Creator | — |
| 27 | The Final Historian Test | Junior Historian | — |
| 28 | The Treasure | Junior Historian | — |
| 29 | My Taj Mahal Discovery Card | Junior Historian | — |
| 30 | Junior Taj Historian Certificate | Junior Historian | — |

---

## Activity Type Distribution

| Activity Type | Pages |
|--------------|-------|
| Map finding / circling | 2, 17 |
| Drawing / completion | 6, 16, 24, 25 |
| Chronology / sequencing | 3, 27 |
| Matching | 5, 9, 12, 22 |
| Maze / route-finding | 15 |
| Spatial placement | 7, 18 |
| Observation | 2, 20, 26 |
| Creative design | 4, 10, 24, 25 |
| Classification / sorting | 21 |
| Labeling | 17 |
| Reasoning | 8, 21, 27 |
| Evidence analysis | 22, 27 |
| Reflection / creative writing | 29 |
| Structural puzzle | 8 |
| Calligraphy practice | 11 |
| Identity / self-introduction | 1 |
| Final assessment | 27 |
| Certificate / reward | 30 |

---

## Open Questions / Design Decisions

> [!IMPORTANT]
> **PDF Generation Method**: Since this environment cannot directly produce a multi-page PDF with embedded fonts and vector graphics, pages will be produced as high-resolution PNG images (8.5×11 at 150dpi = 1275×1650px). A Python script will then combine them into a PDF using `Pillow` or `reportlab`. Please confirm if you have Python available or prefer another export method.

> [!IMPORTANT]
> **Illustration Style**: Pages will be generated using the AI image generator for illustrated scenes, combined with text rendered as document overlays. Some pages (activities, certificates) will be fully rendered as composite images. Key text is always rendered as crisp document text, never inside the AI illustration.

> [!NOTE]
> **Page Production Time**: 30 pages of illustrated, activity-rich content is substantial. The book will be produced in batches of ~5 pages. After each batch, a visual QA check will confirm size, consistency, and quality before continuing.

---

## Verification Plan

### Research Verification
- Cross-reference all dates/facts against UNESCO World Heritage listing, ASI official descriptions, and academic sources
- Flag any disputed or uncertain claims and use cautious wording

### Visual Verification (per batch)
- Confirm 8.5 × 11 in portrait
- Check Taj Mahal has 4 minarets, 1 central dome, correct proportions
- Check no modern elements in historical scenes
- Check explorer character consistency

### Activity Verification
- Every activity has an unambiguous answer in the answer key
- Writing/drawing spaces are adequately sized
- Instructions are complete and clear

### Final Export
- All 30 pages present
- Consistent margins and visual system
- PDF page size verified at 8.5 × 11 in
