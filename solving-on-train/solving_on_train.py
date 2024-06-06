import csv
from datetime import datetime

solve_times = []

csTimer_file_path = "solving-on-train/csTimerExport_20240606_103917.csv"
with open(csTimer_file_path, newline="") as csTimer_export:
    train_solves = csv.reader(csTimer_export, delimiter=";")
    for row in train_solves:
        if row[4] != "Date":
            # 2024-06-03 20:17:48
            solve_time = datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
            print(solve_time)
            solve_times.append(solve_time)

print(solve_times)
arcCard_file_path = "solving-on-train/transaction_export638532887310010632.csv"
with open(arcCard_file_path, newline="") as arcCard_export:
    train_rides = csv.reader(arcCard_export, delimiter=",")
    for ride in train_rides:
        start_time = datetime.now()
        end_time = datetime.now()
        grandate = f"{ride[0]} {ride[1]}"
        if ride[3] == "Pass Use On Entry":
            start_time = datetime.strptime(grandate, "%b-%d-%Y %I:%M %p")
            print("entered: ", start_time)
        elif ride[3] == "Pass Use On Exit":
            print("exited:", ride[1])
            end_time = datetime.strptime(grandate, "%b-%d-%Y %I:%M %p")

        if end_time < start_time:
            print(f"train ride:{start_time} - {end_time}")

        # if ride[3] == "Pass Use On Exit":
        #     grandate = f"{ride[0]} {ride[1]}"
        #     print("exited:", ride[1])
        #     end_time = datetime.strptime(grandate, "%b-%d-%Y %I:%M %p")

        # for solve in solve_times:
        #     if solve < end_time and solve > start_time:
        #         gobbeldy_gook = []
        #         gobbeldy_gook.append(solve)
        #         print("gobbeldy gook", gobbeldy_gook)
