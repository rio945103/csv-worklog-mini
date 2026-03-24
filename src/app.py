from pathlib import Path

from log_utils import (
    append_log,
    input_minutes,
    show_csv_rows,
    show_summary,
    summarize_logs,
)


def main():
    csv_path = Path("data/log.csv")

    date_str = input("日付を入力してください (例: 2026-03-21): ")
    work_str = input("作業内容を入力してください: ")
    minutes = input_minutes()

    append_log(csv_path, date_str, work_str, minutes)

    print()
    print("--- 入力内容 ---")
    print("日付:", date_str)
    print("作業内容:", work_str)
    print("作業時間(分):", minutes)
    print("保存先:", csv_path)
    print("CSVに保存しました。")

    show_csv_rows(csv_path)

    count, total_minutes, daily_count, daily_total_minutes, daily_rows = summarize_logs(
        csv_path, date_str
    )

    show_summary(
        date_str,
        count,
        total_minutes,
        daily_count,
        daily_total_minutes,
        daily_rows,
    )


if __name__ == "__main__":
    main()