#!/usr/bin/env python3
"""Self-test for export_session_traces.py on a synthetic transcript (no real data).

Checks: thinking blocks dropped; secrets and e-mails redacted everywhere;
tool errors/denials get energy 1; Write payloads land in documents.jsonl.
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_session_traces import export  # noqa: E402

SECRET = "hf_" + "A" * 34
LINES = [
    {"type": "user", "message": {"role": "user", "content": f"my token is HUGGINGFACE_TOKEN={SECRET} mail me a@b.org"}},
    {"type": "assistant", "message": {"role": "assistant", "content": [
        {"type": "thinking", "thinking": "PRIVATE REASONING"},
        {"type": "text", "text": "Writing the notes."},
        {"type": "tool_use", "id": "t1", "name": "Write", "input": {"file_path": "/x/LL.md", "content": "# LL\nlesson"}},
        {"type": "tool_use", "id": "t2", "name": "Bash", "input": {"command": "curl -H 'Authorization: Bearer abcdefghijklmnopqrstuvwx'"}},
    ]}},
    {"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": "t1", "content": "File created"},
        {"type": "tool_result", "tool_use_id": "t2", "content": "Permission to use Bash has been denied", "is_error": True},
    ]}},
]


def main():
    fails = []
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "s.jsonl"
        src.write_text("".join(json.dumps(x) + "\n" for x in LINES))
        out = Path(d) / "out"
        counts = export([str(src)], out, 8000, 6)
        blob = "".join((out / f).read_text() for f in ("sft_turns.jsonl", "tool_calls.jsonl", "documents.jsonl"))
        tools = [json.loads(x) for x in (out / "tool_calls.jsonl").read_text().splitlines()]
        docs = [json.loads(x) for x in (out / "documents.jsonl").read_text().splitlines()]
        checks = [
            ("thinking dropped", "PRIVATE REASONING" not in blob and counts["thinking_blocks_dropped"] == 1),
            ("hf token redacted", SECRET not in blob),
            ("bearer redacted", "abcdefghijklmnopqrstuvwx" not in blob),
            ("email redacted", "a@b.org" not in blob),
            ("success energy 0", tools[0]["energy"] == 0.0),
            ("denial energy 1", tools[1]["energy"] == 1.0 and tools[1]["denied"]),
            ("document captured", docs and docs[0]["path"] == "/x/LL.md"),
        ]
        for name, ok in checks:
            print(f"  {'ok  ' if ok else 'FAIL'} {name}")
            if not ok:
                fails.append(name)
    print("PASS" if not fails else f"FAILED {fails}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
