import csv
from datetime import datetime

solve_times = {}

csTimer_file_path = "solving-on-train/csTimerExport_20240607_134110.csv"
with open(csTimer_file_path, newline="") as csTimer_export:
    train_solves = csv.reader(csTimer_export, delimiter=";")
    for row in train_solves:
        if row[4] != "Date":
            # 2024-06-03 20:17:48
            solve_time = datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
            # print(solve_time)
            solve_times[solve_time] = row[1]

print(solve_times)
arcCard_file_path = "solving-on-train/transaction_export638533861219732997.csv"
start_times = []
end_times = []

with open(arcCard_file_path, newline="") as arcCard_export:
    train_rides = csv.reader(arcCard_export, delimiter=",")

    print(train_rides)

    for ride in train_rides:
        if ride[6] == "ETS LRT":
            grandate = f"{ride[0]} {ride[1]}"

            if ride[3] == "Pass Use On Entry":
                start_time = datetime.strptime(grandate, "%b-%d-%Y %I:%M %p")
                start_times.insert(0, start_time)
            elif ride[3] == "Pass Use On Exit":
                end_time = datetime.strptime(grandate, "%b-%d-%Y %I:%M %p")
                end_times.insert(0, end_time)


for i, ride in enumerate(start_times):
    print(f"entered: {start_times[i]}, exited: {end_times[i]}. Solves:")
    for solve in solve_times:
        if solve > start_times[i] and solve < end_times[i]:
            print(solve_times[solve], solve)
