import csv
from datetime import datetime


def get_solve_times(csTimer_file_path):
    solve_times = {}
    with open(csTimer_file_path, newline="") as csTimer_export:
        train_solves = csv.reader(csTimer_export, delimiter=";")
        for row in train_solves:
            if row[4] != "Date":
                # 2024-06-03 20:17:48
                solve_time = datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
                # print(solve_time)
                solve_times[solve_time] = row[1]
    return solve_times


def get_startend_times(arcCard_file_path):
    start_times = []
    end_times = []

    with open(arcCard_file_path, newline="") as arcCard_export:
        train_rides = csv.reader(arcCard_export, delimiter=",")

        for ride in train_rides:
            if ride[6] == "ETS LRT":
                grandate = f"{ride[0]} {ride[1]}"

                if ride[3] == "Pass Use On Entry":
                    start_time = datetime.strptime(grandate, "%b-%d-%Y %I:%M %p")
                    start_times.insert(0, start_time)
                elif ride[3] == "Pass Use On Exit":
                    end_time = datetime.strptime(grandate, "%b-%d-%Y %I:%M %p")
                    end_times.insert(0, end_time)
    return start_times, end_times


def new_func(solve_times, start_time, end_time):
    solvesinride = []
    for solve in solve_times:
        if solve > start_time and solve < end_time:
            solvesinride.append(solve_times[solve])
    return solvesinride


def createdict(solve_times, start_times, end_times):
    # ride_dict = {"happy": "feet", "jappy": "jeet"}
    ride_dict = {}

    for i in range(len(start_times)):
        key = (start_times[i], end_times[i])
        start_time = start_times[i]
        end_time = end_times[i]
        value = new_func(solve_times, start_time, end_time)
        ride_dict[key] = value

    return ride_dict


def time_to_milliseconds(time_str):
    """Convert a time string 'M:SS.ss' to total milliseconds."""
    m, s = time_str.split(":")
    s, ms = s.split(".")
    total_milliseconds = (int(m) * 60 * 1000) + (int(s) * 1000) + (int(ms) * 10)
    return total_milliseconds


def milliseconds_to_time(milliseconds):
    """Convert total milliseconds to a time string 'M:SS.ss'."""
    m = milliseconds // (60 * 1000)
    milliseconds %= 60 * 1000
    s = milliseconds // 1000
    ms = (milliseconds % 1000) // 10
    return f"{m}:{s:02}.{ms:02}"


def mean_time(times):
    """Calculate the mean of a list of times in 'M:SS.ss' format."""
    if not times:
        return None  # or return an appropriate message
    total_milliseconds = [time_to_milliseconds(t) for t in times]
    mean_milliseconds = sum(total_milliseconds) // len(total_milliseconds)
    return milliseconds_to_time(mean_milliseconds)


# Example usage:
times = ["1:20.30", "2:30.45", "0:45.15"]
print(mean_time(times))  # Output should be in "M:SS.ss" format


def main() -> None:
    solve_times = get_solve_times("solving-on-train/csTimerExport_20240607_134110.csv")

    # print(solve_times)
    start_times, end_times = get_startend_times(
        "solving-on-train/transaction_export638533861219732997.csv"
    )
    d = createdict(solve_times, start_times, end_times)
    for i in d:
        print(
            f"entered: {i[0]}, exited: {i[1]}. Solves:\n{d[i]} mo3: {mean_time(d[i])}"
        )

    # for i in range(len(start_times)):
    #     print(f"entered: {start_times[i]}, exited: {end_times[i]}. Solves:")
    #     start_time = start_times[i]
    #     end_time = end_times[i]
    #     print(new_func(solve_times, start_time, end_time))


main()
