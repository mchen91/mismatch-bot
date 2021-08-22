import re


READABLE_TIME_FORMAT = r"^(?:(\d\d?):)?(\d\d?\.\d\d?)$"


def time_string_to_frames(time_string: str):
    time_match = re.fullmatch(READABLE_TIME_FORMAT, time_string)
    if not time_match:
        raise ValueError(f"bad time string {time_string}")
    minutes = time_match.group(1)
    seconds = time_match.group(2)
    time = int(minutes or 0) * 60 + float(seconds)
    return round(time * 60)


def frames_to_time_string(frames: int):
    hours, rem = divmod(frames, 60 * 60 * 60)
    minutes, rem = divmod(rem, 60 * 60)
    seconds, rem = divmod(rem, 60)
    centiseconds = (rem * 99) // 59
    padded_centis = str(centiseconds).zfill(2)
    if hours > 0:
        padded_minutes = str(minutes).zfill(2)
        padded_seconds = str(seconds).zfill(2)
        return f"{hours}:{padded_minutes}:{padded_seconds}.{padded_centis}"
    if minutes > 0:
        padded_seconds = str(seconds).zfill(2)
        return f"{minutes}:{padded_seconds}.{padded_centis}"
    return f"{seconds}.{padded_centis}"
