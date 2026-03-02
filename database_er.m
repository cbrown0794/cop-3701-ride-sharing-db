# Database Relational Schema (Normalized)

Below is the final, BCNF-compliant relational schema derived from the ER diagram, reflecting the physical tables, data types, and constraints that will be implemented in the database.

```mermaid
erDiagram
    DISPATCH_BASE ||--|{ VEHICLE : "manages"
    VEHICLE ||--|| TELEMATICS_TRACKER : "monitors"
    ZONE ||--|{ SURGE_PERIOD : "experiences"
    VEHICLE ||--|{ TRIP : "completes"
    ZONE ||--|{ TRIP : "originates at"

    DISPATCH_BASE {
        VARCHAR(10) BaseCode PK
        VARCHAR(50) BaseName
    }
    VEHICLE {
        VARCHAR(15) VehicleID PK
        VARCHAR(10) LicensePlate UK
        VARCHAR(10) BaseCode FK 
    }
    TELEMATICS_TRACKER {
        VARCHAR(15) TrackerID PK
        VARCHAR(20) FirmwareVersion
        VARCHAR(15) VehicleID FK "UK"
    }
    ZONE {
        INT ZoneID PK
        VARCHAR(50) Borough
    }
    SURGE_PERIOD {
        INT ZoneID PK, FK
        DATETIME StartTime PK
        DECIMAL SurgeMultiplier
    }
    TRIP {
        INT TripID PK
        DATETIME PickupTime
        DATETIME DropoffTime
        DECIMAL FareAmount
        VARCHAR(15) VehicleID FK 
        INT ZoneID FK 
    }
