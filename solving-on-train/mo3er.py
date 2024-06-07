def time_to_ms(time_str):
    """Convert a time string 'M:SS.ss' to total ms."""
    m, s = time_str.split(":")
    s, ms = s.split(".")
    total_ms = (int(m) * 60 * 1000) + (int(s) * 1000) + (int(ms) * 10)
    return total_ms


def ms_to_time(ms):
    """Convert total ms to a time string 'M:SS.ss'."""
    m = ms // (60 * 1000)
    ms %= 60 * 1000
    s = ms // 1000
    ms = (ms % 1000) // 10
    return f"{m}:{s:02}.{ms:02}"


def mean_time(times):
    """Calculate the mean of a list of times in 'M:SS.ss' format."""
    if not times:
        return None
    total_ms = [time_to_ms(t) for t in times]
    mean_ms = sum(total_ms) // len(total_ms)
    return ms_to_time(mean_ms)
