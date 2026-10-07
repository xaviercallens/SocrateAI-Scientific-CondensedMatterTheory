#!/usr/bin/env python3
"""Export Claude Code session transcripts (JSONL) into training data for
retraining / RL / JEPA-style models, in ANSE's trace conventions.

Outputs, in --out (default ~/AutoevolveAI/data/training/adscmt_sessions/):
  sft_turns.jsonl   {session, turn, context:[{role,text}], output:{text, tool_calls}}
  tool_calls.jsonl  {session, tool, input, result, is_error, denied, energy}
                    energy: 0.0 success, 1.0 error or permission denial (lower is better)
  documents.jsonl   every Write-tool payload for a .md/.tex/.py file:
                    {session, path, content}  (the generated text itself)
  MANIFEST.json     sources, counts, scrub statistics

Privacy and hygiene, applied to every string before it is written:
  * model "thinking"/"redacted_thinking" blocks are DROPPED, never exported
  * secrets are replaced: hf_*, ghp_*, github_pat_*, sk-*, Bearer tokens,
    NAME=value for *TOKEN*/*KEY*/*SECRET*/*PASSWORD*, long base64/hex blobs
    after such names, and e-mail addresses (-> <email>)
  * tool results are truncated to --max-result chars
Review MANIFEST.json and a sample before sharing or training on it.

    python3 tools/export_session_traces.py [--out DIR] [transcript.jsonl ...]
    (no files: all transcripts of this project under ~/.claude/projects/)
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from pathlib import Path

SECRET_PATTERNS = [
    (re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"), "<hf-token>"),
    (re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"), "<github-token>"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"), "<github-token>"),
    (re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}\b"), "<api-key>"),
    (re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._\-]{16,}"), "Bearer <token>"),
    (re.compile(r"(?i)\b([A-Z0-9_]*(?:TOKEN|API_KEY|SECRET|PASSWORD)[A-Z0-9_]*)\s*=\s*(['\"]?)[^\s'\"]{8,}\2"),
     r"\1=<redacted>"),
    (re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"), "<email>"),
]
DOC_SUFFIXES = (".md", ".tex", ".py", ".json", ".sh", ".lean", ".bib")


class Scrubber:
    def __init__(self):
        self.hits = 0

    def __call__(self, s):
        if not isinstance(s, str):
            return s
        for pat, rep in SECRET_PATTERNS:
            s, n = pat.subn(rep, s)
            self.hits += n
        return s

    def deep(self, x):
        if isinstance(x, str):
            return self(x)
        if isinstance(x, list):
            return [self.deep(v) for v in x]
        if isinstance(x, dict):
            return {k: self.deep(v) for k, v in x.items()}
        return x


def blocks(message):
    c = (message or {}).get("content")
    if isinstance(c, str):
        return [{"type": "text", "text": c}]
    return c if isinstance(c, list) else []


def result_text(block):
    c = block.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
    return ""


def export(paths, out: Path, max_result: int, context_turns: int):
    out.mkdir(parents=True, exist_ok=True)
    scrub = Scrubber()
    counts = {"sessions": 0, "sft_turns": 0, "tool_calls": 0, "documents": 0, "thinking_blocks_dropped": 0}
    with open(out / "sft_turns.jsonl", "w") as f_sft, open(out / "tool_calls.jsonl", "w") as f_tool, \
            open(out / "documents.jsonl", "w") as f_doc:
        for p in paths:
            session = Path(p).stem
            counts["sessions"] += 1
            history, pending, turn = [], {}, 0
            for line in open(p, encoding="utf-8", errors="replace"):
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                role = rec.get("type")
                if role not in ("user", "assistant"):
                    continue
                texts, calls = [], []
                for b in blocks(rec.get("message")):
                    t = b.get("type")
                    if t in ("thinking", "redacted_thinking"):
                        counts["thinking_blocks_dropped"] += 1
                        continue
                    if t == "text":
                        texts.append(scrub(b.get("text", "")))
                    elif t == "tool_use":
                        inp = scrub.deep(b.get("input", {}))
                        calls.append({"id": b.get("id"), "name": b.get("name"), "input": inp})
                        pending[b.get("id")] = calls[-1]
                        if b.get("name") == "Write" and str(inp.get("file_path", "")).endswith(DOC_SUFFIXES):
                            f_doc.write(json.dumps({"session": session, "path": inp.get("file_path"),
                                                    "content": inp.get("content", "")}, ensure_ascii=False) + "\n")
                            counts["documents"] += 1
                    elif t == "tool_result":
                        call = pending.pop(b.get("tool_use_id"), None)
                        res = scrub(result_text(b))
                        denied = "Permission to use" in res and "denied" in res
                        err = bool(b.get("is_error")) or denied
                        f_tool.write(json.dumps({
                            "session": session, "tool": (call or {}).get("name"), "input": (call or {}).get("input"),
                            "result": res[:max_result], "result_truncated": len(res) > max_result,
                            "is_error": bool(b.get("is_error")), "denied": denied, "energy": 1.0 if err else 0.0,
                        }, ensure_ascii=False) + "\n")
                        counts["tool_calls"] += 1
                        texts.append(f"[tool_result {'ERROR' if err else 'ok'}] {res[:500]}")
                if role == "assistant" and (texts or calls):
                    f_sft.write(json.dumps({
                        "session": session, "turn": turn, "context": history[-context_turns:],
                        "output": {"text": "\n".join(x for x in texts if x),
                                   "tool_calls": [{"name": c["name"], "input": c["input"]} for c in calls]},
                    }, ensure_ascii=False) + "\n")
                    counts["sft_turns"] += 1
                    turn += 1
                summary = "\n".join(x for x in texts if x)
                if calls:
                    summary += "\n" + "\n".join(f"[call {c['name']}]" for c in calls)
                if summary.strip():
                    history.append({"role": role, "text": summary[:4000]})
    counts["secrets_redacted"] = scrub.hits
    (out / "MANIFEST.json").write_text(json.dumps({"sources": [str(p) for p in paths], "counts": counts,
                                                    "format": "see tools/export_session_traces.py docstring"},
                                                   indent=1))
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--out", default=str(Path.home() / "AutoevolveAI" / "data" / "training" / "adscmt_sessions"))
    ap.add_argument("--max-result", type=int, default=8000)
    ap.add_argument("--context-turns", type=int, default=6)
    a = ap.parse_args()
    paths = a.paths or sorted(glob.glob(os.path.expanduser(
        "~/.claude/projects/*SocrateAI-Scientific-CondensedMatterTheory*/*.jsonl")))
    if not paths:
        raise SystemExit("no transcripts found")
    counts = export(paths, Path(a.out), a.max_result, a.context_turns)
    print(json.dumps(counts, indent=1))
    print(f"wrote {a.out}")


if __name__ == "__main__":
    sys.exit(main())
