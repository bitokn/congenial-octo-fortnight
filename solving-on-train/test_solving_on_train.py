import os
import csv
from datetime import datetime, timedelta
from solving_on_train import analyze_solves, print_results

def create_synthetic_cstimer_data(filename):
    """Create synthetic csTimer export data"""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['No.', 'Time', 'Comment', 'Scramble', 'Date', 'DNF?'])
        
        # Create some sample solves during a bus ride
        base_time = datetime(2024, 5, 25, 9, 30)  # 9:30 AM
        for i in range(5):
            solve_time = base_time + timedelta(minutes=i*2)
            writer.writerow([
                i+1,
                "0:15.43",  # solve duration in M:SS.ms format
                "",  # comment
                "R U R' U'",  # scramble
                solve_time.strftime("%Y-%m-%d %H:%M:%S"),
                ""  # DNF
            ])
        
        # Create some sample solves during an LRT ride
        base_time = datetime(2024, 5, 25, 14, 0)  # 2:00 PM
        for i in range(4):
            solve_time = base_time + timedelta(minutes=i*3)
            writer.writerow([
                i+6,
                "0:13.21",  # solve duration in M:SS.ms format
                "",
                "R U R' U'",
                solve_time.strftime("%Y-%m-%d %H:%M:%S"),
                ""
            ])

def create_synthetic_arc_data(filename):
    """Create synthetic ARC card export data"""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Time', 'Location', 'Type', 'Amount', 'Balance', 'Service', 'Details'])
        
        # Morning bus ride
        writer.writerow([
            'May-25-2024',
            '9:25 AM',
            'Stop 1234',
            'Pass Use On Entry',
            '$0.00',
            '$50.00',
            'ETS Local',
            'Regular'
        ])
        writer.writerow([
            'May-25-2024',
            '9:45 AM',
            'Stop 5678',
            'Pass Use On Exit',
            '$0.00',
            '$50.00',
            'ETS Local',
            'Regular'
        ])
        
        # Afternoon LRT ride
        writer.writerow([
            'May-25-2024',
            '1:55 PM',
            'Churchill Station',
            'Pass Use On Entry',
            '$0.00',
            '$50.00',
            'ETS LRT',
            'Regular'
        ])
        writer.writerow([
            'May-25-2024',
            '2:20 PM',
            'Century Park',
            'Pass Use On Exit',
            '$0.00',
            '$50.00',
            'ETS LRT',
            'Regular'
        ])

def test_solving_analysis():
    # Create temporary test files
    cstimer_file = "test_cstimer_export.csv"
    arc_file = "test_arc_export.csv"
    
    try:
        # Generate synthetic data
        create_synthetic_cstimer_data(cstimer_file)
        create_synthetic_arc_data(arc_file)
        
        # Analyze the synthetic data
        results = analyze_solves(cstimer_file, arc_file)
        
        # Print results using the same function as main program
        print("\nTest Results with Synthetic Data:")
        print("=================================")
        print_results(results)
        
        # Test case with no solves
        print("\nTesting case with no solves:")
        print("============================")
        # Create empty csTimer file
        with open(cstimer_file, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['No.', 'Time', 'Comment', 'Scramble', 'Date', 'DNF?'])
        
        empty_results = analyze_solves(cstimer_file, arc_file)
        print_results(empty_results)
            
    finally:
        # Clean up test files
        for file in [cstimer_file, arc_file]:
            if os.path.exists(file):
                os.remove(file)

if __name__ == "__main__":
    test_solving_analysis() 
