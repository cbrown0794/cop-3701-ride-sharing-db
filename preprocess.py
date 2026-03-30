import csv
import random
import os
from datetime import datetime, timedelta

# Make sure this matches the file you extracted!
KAGGLE_FILE = 'uber-raw-data-apr14.csv'
SAMPLE_LIMIT = 1000 # Keeps the DB small enough for Canvas

# Known Uber NYC Base Names mapping
UBER_BASES = {
    'B02512': 'Unter',
    'B02598': 'Hinter',
    'B02617': 'Weiter',
    'B02682': 'Schmecken',
    'B02764': 'Danach-NY'
}

def preprocess_data():
    os.makedirs('data', exist_ok=True)
    
    print(f"Reading real data from {KAGGLE_FILE}...")
    
    raw_trips = []
    unique_bases = set()
    
    # 1. Read real Kaggle Data
    with open(KAGGLE_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= SAMPLE_LIMIT:
                break
            raw_trips.append(row)
            unique_bases.add(row['Base'])

    # 2. Build DISPATCH_BASE from real data + synthetic to reach 100 records
    bases = []
    for b_code in unique_bases:
        bases.append({'BaseCode': b_code, 'BaseName': UBER_BASES.get(b_code, 'Unknown Base')})
    
    # Pad out the bases to hit the 100 record requirement
    for i in range(len(bases), 110):
        bases.append({'BaseCode': f'B9{i:03d}', 'BaseName': f'Simulated_Base_{i}'})

    # 3. Build VEHICLE (>100 records) linked to our Bases
    vehicles = []
    for i in range(1, 150):
        vehicles.append({
            'VehicleID': f'V-{1000+i}',
            'LicensePlate': f'TLC-{1000+i}',
            'BaseCode': random.choice(bases)['BaseCode']
        })

    # 4. Build TELEMATICS_TRACKER (1:1 with Vehicle)
    trackers = []
    for v in vehicles:
        trackers.append({
            'TrackerID': f'TRK-{v["VehicleID"].split("-")[1]}',
            'FirmwareVersion': random.choice(['v1.0.0', 'v1.2.4', 'v2.0.1']),
            'VehicleID': v['VehicleID']
        })

    # 5. Build ZONE (>100 records)
    zones = [{'ZoneID': i, 'Borough': random.choice(['Manhattan', 'Brooklyn', 'Queens', 'Bronx'])} for i in range(1, 120)]

    # 6. Build SURGE_PERIOD
    surges = []
    for i in range(200):
        surges.append({
            'ZoneID': random.choice(zones)['ZoneID'],
            'StartTime': datetime(2014, 4, random.randint(1, 30), random.randint(0, 23), 0, 0).strftime('%Y-%m-%d %H:%M:%S'),
            'SurgeMultiplier': round(random.uniform(1.1, 3.5), 2)
        })
    # Remove duplicates for composite PK
    surges = list({(s['ZoneID'], s['StartTime']): s for s in surges}.values())

    # 7. Build TRIP using real Kaggle timestamps and bases
    trips = []
    for i, raw in enumerate(raw_trips):
        # Parse Kaggle datetime (Format: 4/1/2014 0:11:00)
        try:
            pickup_dt = datetime.strptime(raw['Date/Time'], '%m/%d/%Y %H:%M:%S')
        except ValueError:
            # Fallback if format differs slightly
            pickup_dt = datetime.strptime(raw['Date/Time'], '%m/%d/%Y %H:%M')

        dropoff_dt = pickup_dt + timedelta(minutes=random.randint(5, 45))
        
        # Find a vehicle assigned to this specific real base
        valid_vehicles = [v for v in vehicles if v['BaseCode'] == raw['Base']]
        assigned_vehicle = random.choice(valid_vehicles) if valid_vehicles else random.choice(vehicles)

        trips.append({
            'TripID': i + 1,
            'PickupTime': pickup_dt.strftime('%Y-%m-%d %H:%M:%S'),
            'DropoffTime': dropoff_dt.strftime('%Y-%m-%d %H:%M:%S'),
            'FareAmount': round(random.uniform(8.0, 65.0), 2),
            'VehicleID': assigned_vehicle['VehicleID'],
            'ZoneID': random.choice(zones)['ZoneID']
        })

    # 8. Export to CSV
    datasets = {
        'dispatch_base.csv': (['BaseCode', 'BaseName'], bases),
        'vehicle.csv': (['VehicleID', 'LicensePlate', 'BaseCode'], vehicles),
        'telematics_tracker.csv': (['TrackerID', 'FirmwareVersion', 'VehicleID'], trackers),
        'zone.csv': (['ZoneID', 'Borough'], zones),
        'surge_period.csv': (['ZoneID', 'StartTime', 'SurgeMultiplier'], surges),
        'trip.csv': (['TripID', 'PickupTime', 'DropoffTime', 'FareAmount', 'VehicleID', 'ZoneID'], trips)
    }

    for filename, (fieldnames, data) in datasets.items():
        filepath = os.path.join('data', filename)
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Generated {filepath} with {len(data)} records.")

if __name__ == '__main__':
    preprocess_data()