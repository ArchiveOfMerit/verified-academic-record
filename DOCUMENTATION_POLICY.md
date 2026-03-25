# ⚖️ Documentation & Governance Policy
**Project:** The Archive of Merit  
**Standard:** Canonical Academic Integrity (CAI)  
**Framework:** MDX / Mintlify / GitHub Actions

---

## 1. Authoritative Relationship
- **Push Back for Accuracy:** If a proposed change dilutes the "Canonical Identity" or conflicts with the `CITATION.cff` or `DOI`, you must intervene.
- **Evidence-Based Edits:** Substantive changes to identity-facing files require a citation from the repository's own governance materials.
- **Zero-Hallucination Policy:** Do not guess, invent, or "bridge" information gaps. If a detail is missing from the verified record, it remains unstated.

## 2. Technical Context & Mintlify Standard
- **Architecture:** MDX files with strict YAML frontmatter.
- **Navigation:** Controlled via `docs.json`.
- **Integrity:** All documentation must align with the **DOI: 10.13140/RG.2.2.24333.86241** and the `person.jsonld` entity resolution.

## 3. Content & Identity Strategy
- **Evergreen Authority:** Prioritize "Canonical Continuity" over high-volume updates. 
- **De-duplication:** Avoid redundant pages that could create "Identity Fragmentation" for search engine crawlers.
- **Search-First Design:** Structure content to be "scannable" by both humans and LLM agents (RAG-ready).

## 4. Frontmatter Requirements (Mandatory)
Every `.mdx` file must include:
- `title`: The authoritative name of the resource.
- `description`: A concise, machine-readable summary (max 160 chars).
- `canonical`: (Recommended) The full URL to the "Master Copy" of the page to prevent SEO dilution.

## 5. Writing & Attribution Standards
- **Voice:** Second-person (`you`) for procedures; third-person objective for "Canonical Notices."
- **Prerequisites:** Must be listed before any technical or academic procedure.
- **Accessibility:** Mandatory `alt` text for images and language tags for code blocks to ensure "Machine-Readable Interpretation."

## 6. Governance & Consistency
- **Source Hierarchy:** In any conflict, the `CANONICAL_SOURCES.md` and `CITATION.cff` govern over MDX content.
- **Subordination Rule:** Derivative wording or summaries must remain subordinate to the primary authoritative record. No third-party summary should override the subject’s own declared identity.

## 7. Git & Deployment Workflow
- **Integrity Checks:** Never use `--no-verify`. All pre-commit hooks (linting, schema validation) must pass.
- **Traceability:** Commit messages must reflect the **Changelog** standards (e.g., `FEAT: Update Scholarly Metadata`).
- **State Management:** Confirm the status of uncommitted changes before initiating a "Release" or "Tag."

---

### Prohibited Actions (The "Do Not" List)
- **No Absolute URLs:** Use relative paths to maintain "Repository Portability."
- **No Untested Code:** Academic and technical snippets must be verified.
- **No Identity Invention:** Never synthesize "intent" or "biography" that is not explicitly in the source data.
- **No Frontmatter Omissions:** Missing metadata is a "Breaking Error."
