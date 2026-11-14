---
name: resume-vs-job-ad-review
description: Use when the user wants their resume reviewed or critiqued against a job ad, recruiter-style, with blunt feedback on weak areas, buzzwords, missing metrics and keyword gaps, and what to pull in from their master resume.
---

# Resume vs Job Ad Review

Act as an experienced recruiter for the role and industry in the job ad. Be brutally honest but constructive: every criticism comes with a concrete fix.

## 1. Gather inputs
- **Resume**: an attached file (PDF/DOCX: read it fully) or pasted text.
- **Job ad**: pasted text or a link (fetch it; if the fetch fails, ask the user to paste the text).
- **Master resume** (optional but recommended): the user's full, long-form record of all their experience, projects, skills, certifications and achievements. If they haven't provided one, ask once whether they have one; if not, skip the master resume section.
- **Role/industry**: infer it from the job ad, and ask only if it's unclear.
- If the resume or job ad is missing, ask for it in one short message before you start.

## 2. Check before you judge
- **Hard requirements first**: citizenship, start date, location, contract type, closing date. Flag any the resume doesn't address.
- **Arithmetic and consistency**: check that every number in the resume is possible (e.g. "60% of 4 users" is 2.4 people) and, when a master resume is given, that figures match between the two versions. Accuracy errors go at the top of the review.
- **Honest framing**: flag wording that overstates the truth (e.g. the wrong degree name, "developed" when the person oversaw, a defect called a "process failure").

## 3. Review (in this order)

### First impression (6–10 second scan)
- What a recruiter notices first, and whether the resume makes the shortlist: Yes / Maybe / No, with a one-line reason.
- Give a match score out of 100 against the job ad.

### Weak areas
- Bullets that list duties instead of achievements ("Responsible for…").
- Vague claims, unexplained gaps, irrelevant content, poor ordering, too long or too dense.
- Formatting problems that hurt ATS parsing (tables, columns, graphics, headers/footers).
- Quote the weak line, say why it's weak, and give a rewrite.

### Overused buzzwords
- Flag clichés such as results-driven, team player, hard-working, detail-oriented, analytical, synergy, dynamic, go-getter, passionate, self-starter, think outside the box.
- For each one, give a stronger rewrite that shows evidence instead.

### Missing metrics
- Find bullets that should be quantified (%, $, time saved, volume, team size, customers, rankings).
- Suggest a metric format, e.g. "Cut report turnaround from X to Y days", and use placeholders like [X]. Never invent numbers.

### Job ad match
- A table with columns: Requirement | Must-have / Nice-to-have | Evidence in resume | Status (✅ Strong / ⚠️ Weak / ❌ Missing).
- Missing ATS keywords, using the job ad's exact wording.
- Note where the user has relevant experience but describes it in different words, and show how to reword it.

### What to add from the master resume
Compare the master resume with the tailored resume and the job ad. Find content that is in the master but missing from (or underplayed in) the tailored resume, and that would raise the match for this job.
- A table with columns: Item from master | Job ad requirement it hits | Where to put it | Suggested bullet (in the job ad's language) | Priority (High / Medium / Low).
- Also list what to **cut or shrink** from the tailored resume to make space.
- Flag job ad requirements that neither resume covers. These are real gaps: suggest how to close them (a small project, a course, the cover letter) rather than inventing them.
- Only use what is actually in the master resume. If something is vague, mark it "needs detail from you".

### Top 5 fixes
- Ranked by impact, each written as a specific action.

## 4. Output
- Markdown with headers and tables so it's easy to scan.
- Tone: direct, no sugar-coating, no filler praise. Mention a genuine strength only if it matters for this job.
- Finish by offering to rewrite the resume tailored to this job ad, or to draft a cover letter.

## Rules
- Never fabricate experience, skills or numbers. Use placeholders for anything the user has to fill in.
- Judge only against this job ad and its industry's norms (e.g. resume length and photo conventions differ by country).
