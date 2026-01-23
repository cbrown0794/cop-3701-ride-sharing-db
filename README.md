# Ride-Sharing Demand & Pricing Database

## Project Scope
The goal of this project is to build a robust **Ride Analytics Database** capable of ingesting high-volume ride-sharing data to optimize fleet performance and dynamic pricing strategies. The system will focus on analyzing historical pickup patterns to detect "demand hotspots" (surges) and calculate optimal fare structures.

Since the primary dataset (Uber Pickups in NYC) contains location and time data but lacks explicit fare amounts, this project will include a **pricing engine simulation**. This engine will estimate fares based on time-of-day, demand density, and base pricing models, allowing us to track hypothetical revenue streams alongside actual demand metrics.

### Key Objectives:
1.  **Data Ingestion & Cleaning**: Import millions of pickup records, normalizing timestamps and geolocation data.
2.  **Surge Detection**: Identify high-demand zones by aggregating pickups over specific time windows (e.g., hourly, daily).
3.  **Fare Simulation**: Implement a logic layer to calculate trip costs and surge multipliers based on demand density.
4.  **Performance Optimization**: Create time-based queries to advise on fleet allocation (e.g., "Where should drivers be at 5 PM on a Friday?").

## Users
This database is designed to serve three primary user roles:
* **Fleet Managers**: Who need to know where to position vehicles to minimize wait times and maximize utilization.
* **Pricing Analysts**: Who query the system to understand when and where surge pricing should be triggered to balance supply and demand.
* **Data Engineers**: Who maintain the pipeline and ensure efficient storage of temporal and geospatial data.

## Data Sources
The project relies on real-world data provided by FiveThirtyEight via Kaggle, supplemented by internal lookup tables.

1.  **Primary Dataset**: [Uber Pickups in New York City](https://www.kaggle.com/datasets/fivethirtyeight/uber-pickups-in-new-york-city)
    * **Source**: FiveThirtyEight / Kaggle
    * **Content**: Over 20 million pickup records from 2014-2015.
    * **Key Fields**: `Date/Time`, `Lat`, `Lon`, `Base` (Dispatching Base Code).

2.  **Supplementary/Derived Data**:
    * **Pricing Rules (Simulated)**: A custom table defining base rates ($/mile, $/minute) and surge multipliers derived from pickup density.
    * **NYC Zone Lookup**: Mapping latitude/longitude coordinates to specific NYC boroughs and neighborhoods for regional analysis.
