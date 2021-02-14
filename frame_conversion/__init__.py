import re


READABLE_TIME_FORMAT = r"^(?:(\d\d?):)?(\d\d?\.\d\d?)$"

def time_string_to_frames(time_string):
    time_match = re.fullmatch(READABLE_TIME_FORMAT, time_string)
    if not time_match:
        raise ValueError(f"bad time string {time_string}")
    minutes = time_match.group(1)
    seconds = time_match.group(2)
    time = int(minutes or 0) * 60 + float(seconds)
    return round(time * 60)
