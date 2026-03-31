from src.log_utils import normalize_minutes

from src.log_utils import input_minutes

from src.log_utils import append_log

from src.log_utils import summarize_logs


def test_normalize_minutes_removes_japanese_fun():
    result = normalize_minutes("60分")
    assert result == "60"

def test_normalize_minutes_converts_fullwidth_digits():
    result = normalize_minutes("６０")
    assert result == "60"

def test_normalize_minutes_removes_spaces_and_fun():
    result = normalize_minutes(" 6 0 分 ")
    assert result == "60"

def test_normalize_minutes_removes_fullwidth_spaces():
    result = normalize_minutes("　6 0　分　")
    assert result == "60"

def test_normalize_minutes_keeps_non_numeric_text():
    result = normalize_minutes("abc")
    assert result == "abc"

def test_input_minutes_returns_int(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "60分")

    result = input_minutes()

    assert result == 60

def test_input_minutes_retries_until_valid(monkeypatch):
    inputs = iter(["abc", "60分"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = input_minutes()

    assert result == 60

def test_input_minutes_accepts_fullwidth_digits(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "６０")

    result = input_minutes()

    assert result == 60

def test_input_minutes_accepts_fullwidth_spaces(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "　6 0　分　")

    result = input_minutes()

    assert result == 60

def test_append_log_creates_csv_and_writes_one_row(tmp_path):
    csv_path = tmp_path / "log.csv"

    append_log(csv_path, "2026-03-31", "pytest練習", 60)

    text = csv_path.read_text(encoding="utf-8-sig")

    assert "2026-03-31" in text
    assert "pytest練習" in text
    assert "60" in text

def test_append_log_writes_header_only_once(tmp_path):
    csv_path = tmp_path / "log.csv"

    append_log(csv_path, "2026-03-31", "1件目", 30)
    append_log(csv_path, "2026-04-01", "2件目", 45)

    text = csv_path.read_text(encoding="utf-8-sig")

    assert text.count("日付,作業内容,作業時間(分)") == 1
    assert "2026-03-31,1件目,30" in text
    assert "2026-04-01,2件目,45" in text

def test_summarize_logs_returns_total_minutes(tmp_path):
    csv_path = tmp_path / "log.csv"

    append_log(csv_path, "2026-03-31", "Python", 30)
    append_log(csv_path, "2026-03-31", "pytest", 45)

    total_count, total_minutes, daily_count, daily_total, daily_rows = summarize_logs(csv_path, "2026-03-31")

    assert total_minutes == 75