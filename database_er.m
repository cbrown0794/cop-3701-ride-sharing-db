# Database Entity-Relationship (ER) Diagram

## User Groups
1. **Fleet Managers:** Utilize the system to track `Vehicle` assignments and monitor `Telematics_Tracker` data for utilization.
2. **Pricing Analysts:** Query the `Zone` and `Surge_Period` tables to adjust or simulate pricing algorithms.
3. **Data Engineers / DBAs:** Maintain the ingestion pipeline feeding the massive `Trip` associative table.

## ER Diagram
```mermaid
erDiagram
    DISPATCH_BASE ||--|{ VEHICLE : "manages (1:N)"
    VEHICLE ||--|| TELEMATICS_TRACKER : "monitors (1:1)"
    ZONE ||--|{ SURGE_PERIOD : "experiences (1:N, Identifying)"
    VEHICLE ||--|{ TRIP : "completes (1:N)"
    ZONE ||--|{ TRIP : "originates at (1:N)"

    DISPATCH_BASE {
        string BaseCode PK "Identifier"
        string BaseName "Mandatory"
    }
    VEHICLE {
        string VehicleID PK "Identifier"
        string LicensePlate "Mandatory, Single-value"
        string BaseCode FK 
    }
    TELEMATICS_TRACKER {
        string TrackerID PK "Identifier"
        string FirmwareVersion "Optional"
        string VehicleID FK "Unique"
    }
    ZONE {
        int ZoneID PK "Identifier"
        string Borough "Mandatory"
    }
    SURGE_PERIOD {
        datetime StartTime "Partial Key"
        float SurgeMultiplier "Mandatory"
        int ZoneID FK "Identifying"
    }
    TRIP {
        int TripID PK "Identifier"
        datetime PickupTime "Mandatory"
        datetime DropoffTime "Optional"
        float FareAmount "Single-value"
        string VehicleID FK 
        int ZoneID FK 
    }
