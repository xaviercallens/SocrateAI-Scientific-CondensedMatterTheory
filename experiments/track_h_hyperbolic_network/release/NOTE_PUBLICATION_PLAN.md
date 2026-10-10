# Publication plan for the cylinder note (not executed; needs the user's explicit go-ahead)

Status 2026-10-08: draft built (`paper/note_cylinder.tex`/`.pdf`, 6 pages), committed, **not published**. The user agreed with the
recommendation: a separate short record rather than a v1.3 section, after specialist feedback (`docs/SPECIALIST_OUTREACH.md`) and ideally
after the disk question (card Q5i).

## When the user says go
1. Rebuild from the current data: `python3 paper/make_note_cylinder.py`, then `pdflatex note_cylinder.tex` twice; require 0 undefined
   references and 0 overfull boxes.
2. Gate: `python3 tools/experiment_gate.py` must print ALL PASS; every claim cited (H0-X-0014 to H0-X-0018) must verify against the
   evidence store.
3. Bundle (a **new** Zenodo record, not a new version of the v1.x record, because the note is a different work): the note PDF, the five data
   files of preregistrations 23--27 and the post-hoc diagnostics (labelled), the scripts `exp23`--`exp27` and `paper/make_note_cylinder.py`,
   the preregistrations, and the audit trail files; metadata: type publication/preprint, licence CC BY 4.0 (code MIT), `isSupplementTo`
   10.5281/zenodo.23228685, `references` the Zenodo concept DOI 10.5281/zenodo.23000390 and the GitHub repository.
4. Create the draft with the token wrapper, verify MD5 and metadata exactly as for v1.2 (`release/zenodo_publish.py` refuses on any
   difference), then publish only on the explicit go-ahead, then verify the public record without a token.
5. arXiv (math.NA, cross-list math-ph) needs an endorsement; ask the specialist from the outreach, after their comments.

## Not to do
Do not fold the note into the v1.2 record; do not edit the v1.1 or v1.2 files; do not present the note as a test of holography.
