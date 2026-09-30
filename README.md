# Resume Bot

A folder-based system for keeping one source of truth and producing a tailored resume for each job.

Identity and facts live in `profile.md` and `sections/`. Visual layout lives in `base/`. Each application gets its own folder under `jobs/`. Generated resumes go under `output/` with the same folder name.

## Layout

```
Resume Bot/
├── README.md
├── rules.md
├── profile.md
├── base/
│   └── base_resume.docx
├── sections/
│   ├── experience.md
│   ├── projects.md
│   ├── certificates.md
│   ├── education.md
│   ├── skills.md
│   └── achievements.md
├── jobs/
│   └── 2026-10_Company_Role/
│       ├── posting.md
│       ├── notes.md
│       └── attachments/
└── output/
    └── 2026-10_Company_Role/
        ├── resume_v1.docx
        ├── resume_v1.pdf
        └── changes.md
```

## How to use it

1. Fill in `profile.md` and the files in `sections/`.
2. Keep `base/base_resume.docx` as layout only: headings, order, and fonts. Leave the body empty.
3. For each application, copy `jobs/2026-10_Company_Role/` and rename it `jobs/YYYY-MM_Company_Role/`.
4. Paste the job description into `posting.md`. Put fit, contact, and deadline in `notes.md`. Drop extra files in `attachments/`.
5. Generate the resume into the matching `output/` folder as `resume_v1.docx` and `resume_v1.pdf`, plus `changes.md`. Later revisions use `resume_v2`, and so on. Page limit and regional conventions live in `profile.md`.

## Rules

The bot follows [rules.md](rules.md).
