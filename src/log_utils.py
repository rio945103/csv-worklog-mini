import csv


def normalize_minutes(minutes_str):
    minutes_str = minutes_str.strip()
    minutes_str = minutes_str.replace("分", "")
    minutes_str = minutes_str.replace(" ", "").replace("　", "")
    return minutes_str


def input_minutes():
    while True:
        minutes_str = input("作業時間(分)を入力してください: ")
        result = normalize_minutes(minutes_str)

        try:
            minutes = int(result)
            print(f"OK、{minutes}分で受け付けました。")
            return minutes
        except ValueError:
            print("数字で入力してください。例: 60 / 60分 / ６０分")


def append_log(csv_path, date_str, work_str, minutes):
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = csv_path.exists()

    with open(csv_path, mode="a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["日付", "作業内容", "作業時間(分)"])

        writer.writerow([date_str, work_str, minutes])


def show_csv_rows(csv_path):
    print()
    print("--- CSVの中身 ---")
    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)


def summarize_logs(csv_path, target_date):
    total_minutes = 0
    count = 0
    daily_total_minutes = 0
    daily_count = 0
    daily_rows = []

    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_minutes = int(row["作業時間(分)"])

            total_minutes += row_minutes
            count += 1

            if row["日付"] == target_date:
                daily_total_minutes += row_minutes
                daily_count += 1
                daily_rows.append(row)

    return count, total_minutes, daily_count, daily_total_minutes, daily_rows


def show_summary(target_date, count, total_minutes, daily_count, daily_total_minutes, daily_rows):
    print()
    print("--- 集計 ---")
    print("全件数:", count)
    print("全合計作業時間(分):", total_minutes)
    print("全合計作業時間(時間):", round(total_minutes / 60, 1))

    print()
    print(f"--- {target_date} の集計 ---")
    print("件数:", daily_count)
    print("合計作業時間(分):", daily_total_minutes)
    print("合計作業時間(時間):", round(daily_total_minutes / 60, 1))

    print()
    print(f"--- {target_date} の明細 ---")
    for i, row in enumerate(daily_rows, start=1):
        print(f"{i}. {row['作業内容']} / {row['作業時間(分)']}分")