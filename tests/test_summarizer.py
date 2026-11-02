import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import summarize_transcript as st

from conftest import run_script, std_response


# ---------- unit tests ----------

def test_split_chunks_short_text_returns_one():
    assert st.split_chunks("hello", 100) == ["hello"]


def test_split_chunks_respects_paragraph_boundaries():
    text = "\n\n".join("p" * 40 for _ in range(10))
    chunks = st.split_chunks(text, 100)
    assert len(chunks) == 5
    assert all(len(c) <= 100 for c in chunks)
    assert "".join(c for c in chunks).count("pppp") >= 9


def test_prompts_require_transcript_slot():
    for name, tmpl in st.PROMPTS.items():
        assert "{transcript}" in tmpl, name


def test_missing_transcript_file_exits(capsys):
    with pytest.raises(SystemExit):
        st.main(["does-not-exist.txt"])


# ---------- exercises the HTTP path against a local fake server ----------

def test_chat_sends_valid_payload_and_no_auth_header(monkeypatch):
    captured = {}

    class FakeResp:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self):
            return std_response()

    def fake_urlopen(req, timeout=None):
        import json as _json

        captured["url"] = req.full_url
        captured["headers"] = dict(req.header_items())
        captured["payload"] = _json.loads(req.data.decode())
        return FakeResp()

    monkeypatch.setattr(st.urllib.request, "urlopen", fake_urlopen)
    out = st.chat("http://localhost:11434/v1", "llama3.2:3b", "Say hi", 16384, 5)

    assert out == "MOCK SUMMARY OUTPUT"
    assert captured["url"].endswith("/v1/chat/completions")
    assert captured["payload"]["model"] == "llama3.2:3b"
    assert captured["payload"]["options"]["num_ctx"] == 16384  # ollama default URL bumps context
    headers = {k.lower(): v for k, v in captured["headers"].items()}
    assert "authorization" not in headers  # the whole point: no API key


def test_chat_non_ollama_url_skips_options_and_appends_path(monkeypatch):
    captured = {}

    class FakeResp:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self):
            return std_response()

    def fake_urlopen(req, timeout=None):
        import json as _json

        captured["url"] = req.full_url
        captured["payload"] = _json.loads(req.data.decode())
        return FakeResp()

    mpatch = monkeypatch.setattr
    mpatch(st.urllib.request, "urlopen", fake_urlopen)
    st.chat("http://127.0.0.1:1234/v1", "qwen2.5:7b", "x", 16384, 5)

    assert captured["url"].endswith("/chat/completions")
    assert "options" not in captured["payload"]


def test_chat_url_error_prints_friendly_hint():
    with pytest.raises(SystemExit) as excinfo:
        st.chat("http://localhost:9999/v1", "m", "x", 100, 1)
    assert "ollama" in str(excinfo.value).lower()


# ---------- end-to-end: script talks to a fake OpenAI-compatible endpoint ----------

def test_e2e_summary_via_subprocess(mock_api, tmp_path):
    handler, base = mock_api
    transcript = tmp_path / "meeting.txt"
    transcript.write_text("RAVI: We should ship Tuesday.\n\nDYLAN: Agreed.", encoding="utf-8")
    handler.response = std_response("- Overview: shipping Tuesday")

    result = run_script(str(transcript), "--base-url", base, "--model", "test-model")
    assert result.returncode == 0, result.stderr
    assert "Overview: shipping Tuesday" in result.stdout

    assert len(handler.received) == 1
    body = handler.received[0]
    assert body["model"] == "test-model"
    assert "ship Tuesday" in body["messages"][0]["content"]
    assert "options" not in body  # not an ollama port


def test_e2e_actions_task_uses_actions_prompt(mock_api, tmp_path):
    handler, base = mock_api
    transcript = tmp_path / "meeting.txt"
    transcript.write_text("DYLAN: I will file the permit by Friday.", encoding="utf-8")
    handler.response = std_response("- [x] File permit")

    result = run_script(str(transcript), "--base-url", base, "--task", "actions")
    assert result.returncode == 0, result.stderr
    sent = handler.received[0]["messages"][0]["content"]
    assert "markdown checklist" in sent
    assert "file the permit" in sent


def test_e2e_long_transcript_chunked_and_merged(mock_api, tmp_path):
    handler, base = mock_api
    transcript = tmp_path / "long.txt"
    big = "\n\n".join(f"Paragraph {i:03d}: " + "x" * 90 for i in range(20))
    transcript.write_text(big, encoding="utf-8")
    handler.response = std_response("outline fragment")

    result = run_script(
        str(transcript),
        "--base-url", base,
        "--task", "outline",
        "--max-chars", "300",
    )
    assert result.returncode == 0, result.stderr
    # 20 paragraphs -> ~20 chunks sent, then 1 merge request
    assert len(handler.received) > 3
    final_request = handler.received[-1]["messages"][0]["content"]
    assert "Merge these partial outlines" in final_request
    assert "outline fragment" in result.stdout
