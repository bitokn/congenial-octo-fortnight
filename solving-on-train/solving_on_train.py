import csv
from datetime import datetime, timedelta
from mo3er import mean_time
import matplotlib.pyplot as plt
import numpy as np

# Constants
DEFAULT_RIDE_DURATION = timedelta(minutes=30)  # Default duration when exit time is missing

def get_solve_times(csTimer_file_path):
    solve_times = {}
    print(f"Reading csTimer data from: {csTimer_file_path}")
    with open(csTimer_file_path, newline="") as csTimer_export:
        train_solves = csv.reader(csTimer_export, delimiter=";")
        for row in train_solves:
            if row[4] != "Date":
                try:
                    # Skip DNF solves
                    if row[1].startswith("DNF"):
                        continue
                    
                    # Handle both @ and non-@ formats
                    date_str = row[4].strip()
                    if date_str.startswith("@"):
                        date_str = date_str[1:]  # Remove @ symbol
                    
                    # Check if the year looks correct
                    if "2024-" in date_str:
                        year = int(date_str.split("-")[0])
                        if year > 2024:
                            date_str = f"2023{date_str[4:]}"
                    
                    solve_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    solve_times[solve_time] = row[1]
                except ValueError as e:
                    print(f"Warning: Could not parse date: {row[4]} - Error: {e}")
    
    print(f"Found {len(solve_times)} valid solves")
    return solve_times

def get_startend_times(arcCard_file_path):
    rides = []  # Will store (start_time, end_time, transit_type)
    current_entries = []  # Stack of (time, transit_type) for unmatched entries
    all_records = []  # Store all records to sort them
    
    print(f"Reading ARC card data from: {arcCard_file_path}")
    
    # First, read and parse all records
    with open(arcCard_file_path, newline="") as arcCard_export:
        train_rides = csv.reader(arcCard_export, delimiter=",")
        next(train_rides)  # Skip header row
        for ride in train_rides:
            if ride[6] in ["ETS LRT", "ETS Local"]:
                try:
                    grandate = f"{ride[0]} {ride[1]}"
                    time = datetime.strptime(grandate, "%b-%d-%Y %I:%M %p")
                    transit_type = "LRT" if ride[6] == "ETS LRT" else "Bus"
                    all_records.append((time, transit_type, ride[2], ride[3]))
                except ValueError as e:
                    print(f"Warning: Could not parse date: {grandate} - Error: {e}")
    
    # Sort records chronologically
    all_records.sort(key=lambda x: x[0])
    
    for record in all_records:
        time, transit_type, action, details = record
        
        if details == "Pass Use On Entry":
            current_entries.append((time, transit_type))
        elif details == "Pass Use On Exit":
            # Match this exit with the most recent entry of the same type
            for i in range(len(current_entries) - 1, -1, -1):
                entry_time, entry_type = current_entries[i]
                if entry_type == transit_type and entry_time < time:
                    rides.append((entry_time, time, entry_type))
                    current_entries.pop(i)
                    break
        elif action == "Sales" and "Missing Tap Fare" in details:
            # For missing taps, try to match with any unmatched entry within reasonable time
            if current_entries:
                # Find the most recent entry that's before this time and within 3 hours
                matching_entry_idx = -1
                for i in range(len(current_entries) - 1, -1, -1):
                    entry_time, entry_type = current_entries[i]
                    time_diff = time - entry_time
                    if entry_time < time and time_diff <= timedelta(hours=3):
                        matching_entry_idx = i
                        break
                
                if matching_entry_idx >= 0:
                    entry_time, entry_type = current_entries[matching_entry_idx]
                    rides.append((entry_time, time, entry_type))
                    current_entries.pop(matching_entry_idx)
    
    if current_entries:
        print(f"\nFound {len(current_entries)} unmatched entries")
    
    # Sort rides by start time, most recent first
    rides.sort(reverse=True)
    
    if not rides:
        print("\nNo complete rides found!")
        return [], [], []
    
    # Unzip the sorted rides into separate lists
    start_times, end_times, transit_types = zip(*rides)
    
    print(f"Found {len(rides)} complete rides")
    return list(start_times), list(end_times), list(transit_types)

def create_ride_solves_list(solve_times, start_time, end_time):
    solvesinride = []
    for solve in solve_times:
        if solve > start_time and solve < end_time:
            solvesinride.append(solve_times[solve])
    return solvesinride

def createdict(solve_times, start_times, end_times, transit_types):
    ride_dict = {}
    for i in range(len(start_times)):
        key = (start_times[i], end_times[i], transit_types[i])
        start_time = start_times[i]
        end_time = end_times[i]
        value = create_ride_solves_list(solve_times, start_time, end_time)
        if value:
            ride_dict[key] = value
    return ride_dict

def analyze_solves(csTimer_file_path, arcCard_file_path):
    solve_times = get_solve_times(csTimer_file_path)
    start_times, end_times, transit_types = get_startend_times(arcCard_file_path)
    d = createdict(solve_times, start_times, end_times, transit_types)
    results = []
    for i in d:
        solves = d[i]
        mean = mean_time(solves)
        if mean is not None:
            results.append({
                "transit_type": i[2],
                "entry_time": i[0],
                "exit_time": i[1],
                "solves": solves,
                "mean": mean
            })
    return results, solve_times

def plot_solves_by_time(results):
    # Extract hours and solve times from transit solves only
    hours = []
    times = []
    transit_types = []  # To differentiate between Bus and LRT
    
    for ride in results:
        for solve_str in ride['solves']:
            try:
                # Remove any '+' from the time string
                solve_str = solve_str.replace('+', '')
                
                # Convert solve time string to seconds
                if ':' in solve_str:
                    time_parts = solve_str.split(':')
                    if len(time_parts) == 2:
                        minutes, seconds = time_parts
                        total_seconds = float(minutes) * 60 + float(seconds)
                    else:
                        hours_part, minutes, seconds = time_parts
                        total_seconds = float(hours_part) * 3600 + float(minutes) * 60 + float(seconds)
                else:
                    total_seconds = float(solve_str)
                
                # Get hour of day (0-23)
                entry_time = ride['entry_time']
                hour = entry_time.hour + entry_time.minute / 60.0
                
                hours.append(hour)
                times.append(total_seconds)
                transit_types.append(ride['transit_type'])
            except ValueError as e:
                print(f"Warning: Could not parse solve time: {solve_str}")
                continue
    
    if not hours:
        print("No transit solves found to plot!")
        return
        
    # Create the scatter plot
    plt.figure(figsize=(12, 6))
    
    # Plot points with different colors for Bus vs LRT
    for transit_type in ['Bus', 'LRT']:
        mask = [t == transit_type for t in transit_types]
        if any(mask):
            plt.scatter([h for h, m in zip(hours, mask) if m],
                       [t for t, m in zip(times, mask) if m],
                       alpha=0.6, label=transit_type)
    
    plt.xlabel('Time of Day (24-hour)')
    plt.ylabel('Solve Time (seconds)')
    plt.title('Cube Solve Times During Transit')
    
    # Format x-axis to show hours
    plt.xticks(range(0, 24, 2))
    plt.grid(True, alpha=0.3)
    
    # Add trend line if we have enough points
    if len(hours) > 1:
        z = np.polyfit(hours, times, 1)
        p = np.poly1d(z)
        trend_x = np.array([min(hours), max(hours)])
        plt.plot(trend_x, p(trend_x), "r--", alpha=0.8, label='Trend')
        
        # Calculate average solve time
        avg_time = sum(times) / len(times)
        plt.axhline(y=avg_time, color='g', linestyle=':', alpha=0.8, 
                   label=f'Average ({avg_time:.1f}s)')
    
    plt.legend()
    plt.tight_layout()
    plt.show()

def print_results(results):
    if not results:
        print("\nNo solves with valid means found in any rides!")
        return
        
    for ride in results:
        print(f"\n{ride['transit_type']} Ride:")
        print(f"Time: {ride['entry_time'].strftime('%Y-%m-%d %H:%M')} to {ride['exit_time'].strftime('%H:%M')}")
        print(f"Solves: {len(ride['solves'])} (mean: {ride['mean']})")

if __name__ == "__main__":
    csTimer_data = "./csTimerExport_20250525_215444.csv"
    arc_data = "./transaction_export638838292573963943 copy.csv"
    results, solve_times = analyze_solves(csTimer_data, arc_data)
    print_results(results)
    plot_solves_by_time(results)
