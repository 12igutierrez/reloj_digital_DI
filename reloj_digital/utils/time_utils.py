def seconds_to_hms(seconds: int, show_seconds=True) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60

    if show_seconds:
        return f"{h:02}:{m:02}:{s:02}"
    return f"{h:02}:{m:02}"