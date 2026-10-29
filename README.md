# Resume Ledger

**Your career, recorded once. Your resume, tailored every time.**

Resume Ledger is an agent-driven resume workflow. Keep a structured record of your experience, projects, skills, and achievements; add a job description; and let an AI agent build a tailored, evidence-based resume.

The agent selects relevant facts and drafts the content. A deterministic Python renderer handles the Word layout, PDF export, and page-fit checks.

![Resume Ledger workflow: maintain career facts, add a job posting, let an agent tailor the resume, and render the final PDF](docs/images/flow.gif)

## How it works

1. **Maintain your career ledger.** Add work, projects, skills, education, and achievements to `sections/` as they happen.
2. **Add a job posting.** Create a folder under `jobs/` and put the description or link in `posting.md`.
3. **Let the agent do the work.** The agent reads `AGENTS.md` and `rules.md`, matches the posting against your career record, and drafts `resume.md`.
4. **Build and validate.** The agent runs `tools/render.py` to generate a Word document and PDF, then uses the fit report to refine the resume until it meets the page constraints.
5. **Review the result.** Open the generated resume and `changes.md` to see what was selected, rewritten, omitted, and unsupported by the career record.

The agent owns **content selection and tailoring**. The renderer owns **formatting and page layout**.

## Agent-driven by design

Resume Ledger is designed to be run by an always-on or coding agent that can access the repository and execute Python. The workflow is defined in plain Markdown rather than tied to a specific AI provider:

- `AGENTS.md` is the agent entry point.
- `rules.md` defines the content rules, selection process, and resume constraints.
- Job-posting content is treated as data, not as instructions that can override the rules.
- The agent writes generated files only inside `output/`.
- Each revision is saved as a new version, preserving earlier outputs.

The agent must not invent employers, titles, dates, skills, tools, responsibilities, or metrics. Missing evidence should be reported—not fabricated. Resume Ledger does not submit applications or send resumes anywhere.

## Quick start

### 1. Install requirements

Requires Python 3. On Windows, Microsoft Word exports the PDF. On Linux, LibreOffice does.

### 2. Add your career information

- Update `profile.md` with your contact details and page limit.
- Replace the sample content in `sections/` with your own career history.
- Record full context and outcomes in `sections/my_work.md`; the agent will select and condense relevant details for each role.

Keep the ledger current. It is the source of truth for every resume.

### 3. Add a job

Copy `jobs/_template/` to a new folder, such as `jobs/Company_Role/`. Add the job description or URL to `posting.md`. Use `notes.md` if you want to indicate what to emphasize or leave out.

### 4. Ask the agent to make the resume

Tell the agent: "Build resumes." It follows `AGENTS.md` and `rules.md`, and writes the resume under `output/Company_Role/`.

## Outputs

Each job has its own output directory and version history:

```text
output/Company_Role/v1/
├── resume.md
├── Your_Name_Resume.docx
├── Your_Name_Resume.pdf
└── changes.md
```

- `resume.md` — tailored resume content.
- `.docx` and `.pdf` — rendered resume files.
- `changes.md` — summary of selections, edits, omissions, and evidence gaps.

To revise a resume, ask the agent for changes. It should create `v2` rather than overwrite `v1`. If an evidence gap is reported, update the career ledger with the real information before asking for another version.

## Project structure

```text
Resume Ledger/
├── AGENTS.md              # Agent entry point
├── rules.md               # Selection, wording, and layout rules
├── profile.md             # Contact details and page limit
├── sections/              # Source of truth for career information
│   ├── experience.md
│   ├── my_work.md
│   ├── skills.md
│   ├── education.md
│   ├── certificates.md
│   └── achievements.md
├── jobs/                  # Job postings and optional notes
├── base/                  # Base Word resume template
├── tools/
│   ├── render.py          # Render DOCX/PDF and check page fit
│   └── make_base.py       # Rebuild the base template
├── docs/images/           # Workflow illustration
└── output/                # Generated resumes and version history
```

## Design and rendering

Every resume uses one structure. The words change from job to job. The page does not.

The only sections, in this order, are Education, Experience, Projects, Skills, and Certificates. There is no summary and no achievements section. A section with nothing to say is left off the page. `tools/render.py` rejects any other heading, and it rejects these headings in any other order.

The page is always A4, Times New Roman, with one right-hand column for dates and locations, and 10 pt text on every bullet. Experience bullets may run to 4 lines. Every other bullet may run to 2. An agent building a resume is not allowed to change any of this.

To preview a rendered resume:

```bash
python tools/render.py output/Company_Role/v1/resume.md --preview --max-pages 1
```

The renderer fills `base/base_resume.docx`, asks Microsoft Word (Windows) or LibreOffice (Linux) to export a PDF, and measures that PDF for the page-fit check. Install Times New Roman on Linux so LibreOffice can match the page.

### Changing the structure

Change it only when you want every future resume to look different. Resumes already rendered stay as they are.

1. Edit the constants at the top of `tools/make_base.py`. `SECTIONS` is the section names and their order. The other constants are the page: margins, font, sizes, line spacing, and where the date column sits.
2. Rebuild the template:

```bash
python tools/make_base.py
```

3. Update section 7 of `rules.md` so the agent writes the new shape. The script only accepts headings that are in the template.

A new section name is not enough if the lines inside it should work differently. The 4-line limit is hardcoded in `tools/render.py` for a section named Experience. A two-column layout, a photo, or a summary with its own line style means changing that script as well, not only the template. Do not edit `base/base_resume.docx` by hand. The next rebuild overwrites it.

## Core principle

**One maintained career record. A separate, tailored resume for every opportunity. No invented claims.**
