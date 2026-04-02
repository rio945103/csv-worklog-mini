from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import app


def test_main_calls_functions_with_expected_values(monkeypatch):
    calls = []

    inputs = iter(["2026-04-02", "pytest学習"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr(app, "input_minutes", lambda: 60)

    def fake_append_log(csv_path, date_str, work_str, minutes):
        calls.append(("append_log", csv_path, date_str, work_str, minutes))

    def fake_show_csv_rows(csv_path):
        calls.append(("show_csv_rows", csv_path))

    def fake_summarize_logs(csv_path, date_str):
        calls.append(("summarize_logs", csv_path, date_str))
        return 1, 60, 1, 60, [
            {"日付": "2026-04-02", "作業内容": "pytest学習", "作業時間(分)": "60"}
        ]

    def fake_show_summary(
        date_str,
        count,
        total_minutes,
        daily_count,
        daily_total_minutes,
        daily_rows,
    ):
        calls.append((
            "show_summary",
            date_str,
            count,
            total_minutes,
            daily_count,
            daily_total_minutes,
            daily_rows,
        ))

    monkeypatch.setattr(app, "append_log", fake_append_log)
    monkeypatch.setattr(app, "show_csv_rows", fake_show_csv_rows)
    monkeypatch.setattr(app, "summarize_logs", fake_summarize_logs)
    monkeypatch.setattr(app, "show_summary", fake_show_summary)

    app.main()

    assert calls[0] == (
        "append_log",
        Path("data/log.csv"),
        "2026-04-02",
        "pytest学習",
        60,
    )
    assert calls[1] == ("show_csv_rows", Path("data/log.csv"))
    assert calls[2] == ("summarize_logs", Path("data/log.csv"), "2026-04-02")
    assert calls[3][0] == "show_summary"
    assert calls[3][1] == "2026-04-02"
    assert calls[3][2] == 1
    assert calls[3][3] == 60
    assert calls[3][4] == 1
    assert calls[3][5] == 60
    assert calls[3][6][0]["作業内容"] == "pytest学習"

def test_main_prints_input_summary(monkeypatch, capsys):
    inputs = iter(["2026-04-02", "pytest学習"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr(app, "input_minutes", lambda: 60)

    monkeypatch.setattr(app, "append_log", lambda *args: None)
    monkeypatch.setattr(app, "show_csv_rows", lambda *args: None)
    monkeypatch.setattr(
        app,
        "summarize_logs",
        lambda csv_path, date_str: (1, 60, 1, 60, []),
    )
    monkeypatch.setattr(app, "show_summary", lambda *args: None)

    app.main()

    captured = capsys.readouterr()

    assert "--- 入力内容 ---" in captured.out
    assert "2026-04-02" in captured.out
    assert "pytest学習" in captured.out
    assert "60" in captured.out
    assert "data\\log.csv" in captured.out or "data/log.csv" in captured.out
    assert "CSVに保存しました。" in captured.out

def test_main_creates_real_csv_file(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    inputs = iter(["2026-04-03", "統合テスト", "60分"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    app.main()

    csv_path = tmp_path / "data" / "log.csv"

    assert csv_path.exists()

    text = csv_path.read_text(encoding="utf-8-sig")
    assert "2026-04-03" in text
    assert "統合テスト" in text
    assert "60" in text

def test_main_retries_invalid_minutes_and_then_saves(monkeypatch, tmp_path, capsys):
    monkeypatch.chdir(tmp_path)

    inputs = iter(["2026-04-04", "再入力確認", "abc", "60分"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    app.main()

    captured = capsys.readouterr()
    csv_path = tmp_path / "data" / "log.csv"

    assert "数字で入力してください。" in captured.out
    assert csv_path.exists()

    text = csv_path.read_text(encoding="utf-8-sig")
    assert "2026-04-04" in text
    assert "再入力確認" in text
    assert "60" in text

def test_main_appends_rows_when_run_twice(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    inputs = iter([
        "2026-04-05", "1回目作業", "30分",
        "2026-04-06", "2回目作業", "45分",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    app.main()
    app.main()

    csv_path = tmp_path / "data" / "log.csv"

    assert csv_path.exists()

    text = csv_path.read_text(encoding="utf-8-sig")
    assert text.count("日付,作業内容,作業時間(分)") == 1
    assert "2026-04-05,1回目作業,30" in text
    assert "2026-04-06,2回目作業,45" in text