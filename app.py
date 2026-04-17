import streamlit as st
import sqlite3

# --- DATABASE SETUP ---
DB_NAME = "ride_sharing.db"

# --- STREAMLIT UI ---
st.title("Ride-Sharing Demand & Pricing Database")
st.subheader("Table Operations")

menu = ["List All Trips", "List Trips by Base of Origin", "List Number of Trips by Zone", 
    "List Trips Greater Than an Amount", "List Trips Done by One Vehicle"]
choice = st.sidebar.selectbox("Select Action", menu)

# --- List all trips ---
if choice == "List All Trips":
    st.write("### Trip List")
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cur.execute("SELECT t.TripID, t.PickupTime, t.DropoffTime, t.FareAmount, t.VehicleID, z.Borough FROM trip t LEFT JOIN zone z ON t.ZoneID = z.ZoneID")
        data = cur.fetchall()
        cur.close()
        conn.close()

        if data:
            st.table(data)
        else:
            st.info("No records found.")
    except Exception as e:
        st.error(f"Error: {e}")

# --- List all trips by base ---
if choice == "List Trips by Base of Origin":
    st.write("### Trips by Base")
    bcode = st.text_input("Base Code (Format: B9XXX or B02512)")
    if st.button("Show Trips"):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cur.execute("SELECT * FROM trip WHERE VehicleID IN (SELECT VehicleID FROM vehicle WHERE BaseCode = ?)", (bcode,))
            data = cur.fetchall()
            cur.close()
            conn.close()

            if data:
                st.table(data)
            else:
                st.info("No records found. Try a different base ID.")
        except Exception as e:
            st.error(f"Error: {e}")
            
# --- List number of trips by zone ---
if choice == "List Number of Trips by Zone":
    st.write("### Number of Trips by Zone")
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cur.execute("SELECT ZoneID, COUNT(*) AS Count FROM trip GROUP BY ZoneID")
        data = cur.fetchall()
        cur.close()
        conn.close()

        if data:
            st.table(data)
        else:
            st.info("No records found.")
    except Exception as e:
        st.error(f"Error: {e}")

# --- List all trips greater than a specified fare amount ---
if choice == "List Trips Greater Than an Amount":
    st.write("### Trips More Expensive Than an Amount")
    fare = st.text_input("Fare Amount (At most 6 figures and 2 decimals)")
    if st.button("Show Trips"):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cur.execute("SELECT * FROM trip WHERE FareAmount > ?", (fare,))
            data = cur.fetchall()
            cur.close()
            conn.close()

            if data:
                st.table(data)
            else:
                st.info("No records found. Try a different fare amount.")
        except Exception as e:
            st.error(f"Error: {e}")

# --- List all trips by one vehicle ---
if choice == "List Trips Done by One Vehicle":
    st.write("### Trips Done by a Vehicle")
    vid = st.text_input("Vehicle ID (Format: V-XXXX)")
    if st.button("Show Trips"):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cur.execute("SELECT t.TripID, t.PickupTime, t.DropoffTime, t.FareAmount, t.ZoneID, v.LicensePlate FROM trip t LEFT JOIN vehicle v ON t.VehicleID = v.VehicleID WHERE t.VehicleID = ?", (vid,))
            data = cur.fetchall()
            cur.close()
            conn.close()

            if data:
                st.table(data)
            else:
                st.info("No records found. Try a different vehicle ID.")
        except Exception as e:
            st.error(f"Error: {e}")
