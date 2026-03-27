from src.log_utils import normalize_minutes


def test_normalize_minutes_removes_japanese_fun():
    result = normalize_minutes("60分")
    assert result == "60"