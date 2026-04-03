from src.log_utils import normalize_minutes

from src.log_utils import input_minutes

from src.log_utils import append_log

from src.log_utils import summarize_logs

from src.log_utils import show_csv_rows

from src.log_utils import show_summary

from src.log_utils import (
    append_log,
    input_date,
    input_minutes,
    normalize_minutes,
    show_csv_rows,
    show_summary,
    summarize_logs,
)

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

def test_summarize_logs_returns_daily_total_for_target_date(tmp_path):
    csv_path = tmp_path / "log.csv"

    append_log(csv_path, "2026-03-30", "前日作業", 20)
    append_log(csv_path, "2026-03-31", "Python", 30)
    append_log(csv_path, "2026-03-31", "pytest", 45)

    total_count, total_minutes, daily_count, daily_total, daily_rows = summarize_logs(csv_path, "2026-03-31")

    assert daily_total == 75

def test_summarize_logs_returns_daily_rows_for_target_date(tmp_path):
    csv_path = tmp_path / "log.csv"

    append_log(csv_path, "2026-03-30", "前日作業", 20)
    append_log(csv_path, "2026-03-31", "Python", 30)
    append_log(csv_path, "2026-03-31", "pytest", 45)

    total_count, total_minutes, daily_count, daily_total, daily_rows = summarize_logs(csv_path, "2026-03-31")

    assert len(daily_rows) == 2
    assert daily_rows[0]["日付"] == "2026-03-31"
    assert daily_rows[0]["作業内容"] == "Python"
    assert daily_rows[0]["作業時間(分)"] == "30"
    assert daily_rows[1]["日付"] == "2026-03-31"
    assert daily_rows[1]["作業内容"] == "pytest"
    assert daily_rows[1]["作業時間(分)"] == "45"

def test_summarize_logs_returns_daily_count_for_target_date(tmp_path):
    csv_path = tmp_path / "log.csv"

    append_log(csv_path, "2026-03-30", "前日作業", 20)
    append_log(csv_path, "2026-03-31", "Python", 30)
    append_log(csv_path, "2026-03-31", "pytest", 45)

    total_count, total_minutes, daily_count, daily_total, daily_rows = summarize_logs(csv_path, "2026-03-31")

    assert daily_count == 2

def test_summarize_logs_returns_total_count(tmp_path):
    csv_path = tmp_path / "log.csv"

    append_log(csv_path, "2026-03-30", "前日作業", 20)
    append_log(csv_path, "2026-03-31", "Python", 30)
    append_log(csv_path, "2026-03-31", "pytest", 45)

    total_count, total_minutes, daily_count, daily_total, daily_rows = summarize_logs(csv_path, "2026-03-31")

    assert total_count == 3

def test_summarize_logs_returns_total_minutes_across_all_dates(tmp_path):
    csv_path = tmp_path / "log.csv"

    append_log(csv_path, "2026-03-30", "前日作業", 20)
    append_log(csv_path, "2026-03-31", "Python", 30)
    append_log(csv_path, "2026-03-31", "pytest", 45)

    total_count, total_minutes, daily_count, daily_total, daily_rows = summarize_logs(csv_path, "2026-03-31")

    assert total_minutes == 95

def test_summarize_logs_returns_zero_when_target_date_has_no_rows(tmp_path):
    csv_path = tmp_path / "log.csv"

    append_log(csv_path, "2026-03-30", "前日作業", 20)
    append_log(csv_path, "2026-03-31", "Python", 30)

    total_count, total_minutes, daily_count, daily_total, daily_rows = summarize_logs(csv_path, "2026-04-01")

    assert daily_count == 0
    assert daily_total == 0
    assert daily_rows == []

def test_summarize_logs_keeps_total_values_even_when_target_date_has_no_rows(tmp_path):
    csv_path = tmp_path / "log.csv"

    append_log(csv_path, "2026-03-30", "前日作業", 20)
    append_log(csv_path, "2026-03-31", "Python", 30)

    total_count, total_minutes, daily_count, daily_total, daily_rows = summarize_logs(csv_path, "2026-04-01")

    assert total_count == 2
    assert total_minutes == 50

def test_summarize_logs_returns_all_zero_for_header_only_csv(tmp_path):
    csv_path = tmp_path / "log.csv"
    csv_path.write_text("日付,作業内容,作業時間(分)\n", encoding="utf-8-sig")

    total_count, total_minutes, daily_count, daily_total, daily_rows = summarize_logs(csv_path, "2026-04-01")

    assert total_count == 0
    assert total_minutes == 0
    assert daily_count == 0
    assert daily_total == 0
    assert daily_rows == []

def test_summarize_logs_with_missing_csv_file(tmp_path):
    csv_path = tmp_path / "missing.csv"

    total_count, total_minutes, daily_count, daily_total, daily_rows = summarize_logs(csv_path, "2026-04-01")

    assert total_count == 0
    assert total_minutes == 0
    assert daily_count == 0
    assert daily_total == 0
    assert daily_rows == []

def test_append_log_accepts_string_path(tmp_path):
    csv_path = tmp_path / "log.csv"

    append_log(str(csv_path), "2026-04-01", "文字列パス確認", 15)

    text = csv_path.read_text(encoding="utf-8-sig")

    assert "2026-04-01" in text
    assert "文字列パス確認" in text
    assert "15" in text

def test_summarize_logs_accepts_string_path(tmp_path):
    csv_path = tmp_path / "log.csv"

    append_log(csv_path, "2026-04-01", "文字列パス集計", 25)

    total_count, total_minutes, daily_count, daily_total, daily_rows = summarize_logs(str(csv_path), "2026-04-01")

    assert total_count == 1
    assert total_minutes == 25
    assert daily_count == 1
    assert daily_total == 25
    assert daily_rows[0]["作業内容"] == "文字列パス集計"

def test_show_csv_rows_prints_saved_rows(tmp_path, capsys):
    csv_path = tmp_path / "log.csv"

    append_log(csv_path, "2026-04-01", "表示確認", 25)

    show_csv_rows(csv_path)

    captured = capsys.readouterr()

    assert "2026-04-01" in captured.out
    assert "表示確認" in captured.out
    assert "25" in captured.out

def test_show_summary_prints_summary_values(capsys):
    show_summary("2026-03-31", 3, 95, 2, 75, [
        {"日付": "2026-03-31", "作業内容": "Python", "作業時間(分)": "30"},
        {"日付": "2026-03-31", "作業内容": "pytest", "作業時間(分)": "45"},
    ])

    captured = capsys.readouterr()

    assert "2026-03-31" in captured.out
    assert "3" in captured.out
    assert "95" in captured.out
    assert "2" in captured.out
    assert "75" in captured.out
    assert "Python" in captured.out
    assert "pytest" in captured.out

def test_show_summary_prints_zero_daily_values_when_no_target_rows(capsys):
    show_summary("2026-04-01", 2, 50, 0, 0, [])

    captured = capsys.readouterr()

    assert "2026-04-01" in captured.out
    assert "2" in captured.out
    assert "50" in captured.out

def test_show_csv_rows_with_missing_csv_file(tmp_path, capsys):
    csv_path = tmp_path / "missing.csv"

    show_csv_rows(csv_path)

    captured = capsys.readouterr()

    assert captured.out is not None

def test_show_csv_rows_with_header_only_csv(tmp_path, capsys):
    csv_path = tmp_path / "log.csv"
    csv_path.write_text("日付,作業内容,作業時間(分)\n", encoding="utf-8-sig")

    show_csv_rows(csv_path)

    captured = capsys.readouterr()

    assert "--- CSVの中身 ---" in captured.out

def test_show_csv_rows_prints_message_when_csv_file_is_missing(tmp_path, capsys):
    csv_path = tmp_path / "missing.csv"

    show_csv_rows(csv_path)

    captured = capsys.readouterr()

    assert "--- CSVの中身 ---" in captured.out
    assert "CSVファイルがまだありません。" in captured.out

def test_show_csv_rows_accepts_string_path(tmp_path, capsys):
    csv_path = tmp_path / "log.csv"

    append_log(csv_path, "2026-04-01", "文字列パス表示", 10)

    show_csv_rows(str(csv_path))

    captured = capsys.readouterr()

    assert "2026-04-01" in captured.out
    assert "文字列パス表示" in captured.out
    assert "10" in captured.out

def test_append_log_creates_parent_directories(tmp_path):
    csv_path = tmp_path / "data" / "logs" / "log.csv"

    append_log(csv_path, "2026-04-01", "親フォルダ作成確認", 20)

    assert csv_path.exists()
    text = csv_path.read_text(encoding="utf-8-sig")
    assert "2026-04-01" in text
    assert "親フォルダ作成確認" in text
    assert "20" in text

def test_append_log_accepts_string_path_and_creates_parent_directories(tmp_path):
    csv_path = tmp_path / "data" / "logs" / "log.csv"

    append_log(str(csv_path), "2026-04-02", "文字列パス親フォルダ確認", 35)

    assert csv_path.exists()
    text = csv_path.read_text(encoding="utf-8-sig")
    assert "2026-04-02" in text
    assert "文字列パス親フォルダ確認" in text
    assert "35" in text

def test_input_date_returns_valid_date(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "2026-04-02")

    result = input_date()

    assert result == "2026-04-02"

def test_input_date_retries_until_valid(monkeypatch, capsys):
    inputs = iter(["2026/04/02", "2026-04-02"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = input_date()

    captured = capsys.readouterr()

    assert result == "2026-04-02"
    assert "日付は YYYY-MM-DD 形式で入力してください。" in captured.out