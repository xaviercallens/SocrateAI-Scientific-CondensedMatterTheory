# Pending Zenodo publication: version 1.2

Created 2026-10-08 00:0x UTC by the session, on the user's instruction of 2026-10-07 ("publish on Zenodo tomorrow
morning with the last research works"). Scheduled publish step: 2026-10-08 06:41 UTC.

| Field | Value |
|---|---|
| New-version draft (deposition id) | 23228685 |
| Reserved DOI | 10.5281/zenodo.23228685 |
| Concept DOI | 10.5281/zenodo.23000390 |
| Previous version | v1.1, 10.5281/zenodo.23002378 |
| Built from commit | ccfc30dddab42c801d7aedb7d0ff99e0fff4139b |
| Bundle | `release/build/zenodo/` from `python3 release/export.py --v12`; `check_bundle.py`: all checks pass |

MD5 of the uploaded files (local copies; `zenodo_publish.py` re-verifies against the draft before publishing):

| File | MD5 | Bytes |
|---|---|---|
| paper.pdf | 0662bfe4e948f9853edffe6791db373d | 481731 |
| dataset.zip | 10de7fb459a2d200fc01e5b623bebf81 | 997803 |
| code.zip | b32781f3a56f93081c1c1f138918eabc | 536221 |

Publish command (irreversible): `bash release/publish.sh publish 23228685`, then `bash release/publish.sh hf`.
Preconditions: `git diff --stat ccfc30d HEAD` touches nothing outside `release/PENDING_ZENODO.md`, `docs/`, `LL.md`
and `*.md` result files (i.e. nothing that enters the bundle: no `data/`, `paper/`, scripts or `release/export.py`);
and the three local MD5s match this table. If either fails, do not publish; rebuild and re-draft instead.
After publishing: add the Version 1.2 block to `PUBLISHED.md`, put the DOI in `RELEASE_NOTES_v1.2.md`, delete this file.
