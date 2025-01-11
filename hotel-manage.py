import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import smtplib
from dotenv import load_dotenv
import os
from streamlit_option_menu import option_menu

load_dotenv()

# Database setup
conn = sqlite3.connect("hotel_management.db", check_same_thread=False)
cursor = conn.cursor()

def about_us_page():
    st.markdown(
        """
        <div style="text-align: center; padding: 20px; background-color: #222233; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);">
            <h1 style="color: #00c8ff; font-size: 48px; margin-bottom: 10px;">About Us</h1>
            <p style="font-size: 20px; color: #e0e0e0; margin-bottom: 30px;">
                I am a passionate web developer dedicated to crafting innovative and user-friendly digital solutions
            </p>
            <div style="background-color: #1e1e2f; padding: 20px; border-radius: 8px; margin: 0 auto; width: 60%; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);">
                <p style="font-size: 18px; color: #ffffff;"><b>Developer Name :</b> Rishabh Yadav</p>
                <p style="font-size: 18px; color: #ffffff;"><b>Contact:</b> <a href="mailto:yrishabh325@gmail.com" style="color: #00c8ff; text-decoration: none;">yrishabh325@gmail.com</a></p>
            </div>
            <h2 style="color: #00c8ff; font-size: 28px; font-weight: bold; margin-bottom: 20px;">Connect with me on : </h2>
            <div style="margin-top: 20px;">
                <a href="https://www.instagram.com/rishabh_yadav_1302/" target="_blank" style="margin-right: 10px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174855.png" alt="Instagram" width="40" height="40">
                </a>
                <a href="https://www.linkedin.com/in/rishabh-yadav-40a288289/" target="_blank" style="margin-right: 10px; margin-left: 10px">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" width="40" height="40">
                </a>
                <a href="https://www.facebook.com/profile.php?id=100012021993965" target="_blank" style="margin-right: 10px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174848.png" alt="Facebook" width="40" height="40">
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(name, email, message):
    """Send an email with the feedback details."""
    try:
        # Establish connection to the email server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            # Create email content
            subject = "New Feedback Received"
            body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            email_message = f"Subject: {subject}\n\n{body}"

            # Send email
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, email_message)  # To: Yourself
    except Exception as e:
        st.error(f"Error sending email: {e}")

def contact_us_page():
    """Contact Us page where users can send feedback."""
    st.markdown(
        """
        <div style="text-align: center; padding: 20px; background-color: #222233; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);">
            <h1 style="color: #00c8ff; font-size: 48px; margin-bottom: 10px;">Contact Us</h1>
            <p style="font-size: 20px; color: #e0e0e0; margin-bottom: 30px;">
                We value your feedback and suggestions. Feel free to reach out to us!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Input fields
    name = st.text_input("Name", placeholder="Enter your name")
    email = st.text_input("Email", placeholder="Enter your email")
    message = st.text_area("Message", placeholder="Write your message here")

    # Submit button
    if st.button("Send Feedback"):
        if not name or not email or not message:
            st.warning("Please fill in all the fields.")
        else:
            send_email(name, email, message)
            st.success("Thank you for your feedback!")

st.markdown("""
<style>
    .record-container {
        background-color: #2c2c2c;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        font-family: 'Arial', sans-serif;
        color: #f5f5f5;
    }
    .record-header {
        font-size: 20px;
        font-weight: bold;
        color: #e0e0e0;
        margin-bottom: 10px;
    }
    .record-body {
        font-size: 16px;
        color: #cfcfcf;
    }
    .record-body strong {
        color: #f5a623;
    }
</style>
""", unsafe_allow_html=True)



# Create tables if not exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_type TEXT,
    price_per_night REAL,
    availability TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    room_id INTEGER,
    checkin_date TEXT,
    checkout_date TEXT,
    total_cost REAL,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS food_orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER,
    items TEXT,
    total_cost REAL,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
)
''')

conn.commit()

# Insert sample data
cursor.execute("SELECT COUNT(*) FROM rooms")
if cursor.fetchone()[0] == 0:
    rooms = [
        ("Single", 1000, "Available"),
        ("Double", 2000, "Available"),
        ("Suite", 5000, "Available"),
    ]
    cursor.executemany("INSERT INTO rooms (room_type, price_per_night, availability) VALUES (?, ?, ?)", rooms)
    conn.commit()

# Streamlit GUI
st.title("The Grand Horizon")

# Navigation


def room_query(cursor):
    st.header("Room Type Query")
    cursor.execute("SELECT room_id, room_type, price_per_night, availability FROM rooms")
    rooms = cursor.fetchall()
    for room in rooms:
        st.markdown(f"""
        <div style="
            background-color: #1e1e1e; 
            padding: 20px; 
            border-radius: 12px; 
            margin-bottom: 15px; 
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5); 
            font-family: 'Arial', sans-serif; 
            color: #f5f5f5;">
            <h4 style="margin: 0; color: #f5a623;">Room ID: {room[0]}</h4>
            <p><strong>Type:</strong> {room[1]}</p>
            <p><strong>Price:</strong> ₹{room[2]:,.2f}</p>
            <p><strong>Available:</strong> {"Yes" if room[3] else "No"}</p>
        </div>
        """, unsafe_allow_html=True)

def book_room(cursor, conn):
    st.header("Room Booking")
    name = st.text_input("Enter your name")
    cursor.execute("SELECT room_type FROM rooms WHERE availability = 'Available'")
    available_rooms = [row[0] for row in cursor.fetchall()]
    room_type = st.selectbox("Select Room Type", available_rooms)
    checkin_date = st.date_input("Check-in Date")
    checkout_date = st.date_input("Check-out Date")
    if st.button("Book Room"):
        if checkout_date <= checkin_date:
            st.error("Check-out date must be after check-in date!")
        else:
            cursor.execute("SELECT room_id, price_per_night FROM rooms WHERE room_type = ? AND availability = 'Available'", (room_type,))
            room = cursor.fetchone()
            if room:
                room_id, price_per_night = room
                days = (checkout_date - checkin_date).days
                total_cost = days * price_per_night
                cursor.execute("INSERT INTO bookings (name, room_id, checkin_date, checkout_date, total_cost) VALUES (?, ?, ?, ?, ?)",
                               (name, room_id, checkin_date, checkout_date, total_cost))
                cursor.execute("UPDATE rooms SET availability = 'Booked' WHERE room_id = ?", (room_id,))
                conn.commit()
                st.success(f"Room booked successfully! Total cost: ₹{total_cost}")
            else:
                st.error("Room not available!")

def check_in(cursor, conn):
    st.header("Check-in")
    booking_id = st.text_input("Enter Booking ID")
    if st.button("Check-in"):
        cursor.execute("SELECT booking_id FROM bookings WHERE booking_id = ?", (booking_id,))
        if cursor.fetchone():
            cursor.execute("UPDATE rooms SET availability = 'Checked-in' WHERE room_id = (SELECT room_id FROM bookings WHERE booking_id = ?)", (booking_id,))
            conn.commit()
            st.success("Check-in successful!")
        else:
            st.error("Booking ID not found!")

def check_out(cursor, conn):
    st.header("Check-out")
    booking_id = st.text_input("Enter Booking ID")
    if st.button("Check-out"):
        cursor.execute("SELECT booking_id FROM bookings WHERE booking_id = ?", (booking_id,))
        if cursor.fetchone():
            cursor.execute("UPDATE rooms SET availability = 'Available' WHERE room_id = (SELECT room_id FROM bookings WHERE booking_id = ?)", (booking_id,))
            conn.commit()
            st.success("Check-out successful!")
        else:
            st.error("Booking ID not found!")

# Similarly, define functions for Order Food, Generate Bill, and Records...
def order_food(cursor, conn):
    st.header("Food Ordering/Room Service")
    
    booking_id = st.text_input("Enter Booking ID")
    
    # Expanded food menu with prices included in the display
    food_prices = {
        "Burger": 299, 
        "Pizza": 599, 
        "Pasta": 399, 
        "Salad": 199, 
        "Soda": 99, 
        "Fries": 149, 
        "Sandwich": 249, 
        "Grilled Chicken": 499, 
        "Paneer Tikka": 399, 
        "Brownie with Ice Cream": 249, 
        "Coffee": 99, 
        "Tea": 79
    }
    
    # Creating a list with names and prices for display
    food_items_with_prices = [f"{item} - ₹{price}" for item, price in food_prices.items()]
    
    # Dropdown menu with items and prices
    selected_food = st.selectbox("Select Food Item (Price Included)", food_items_with_prices)
    
    # Extract the food item name from the selected item
    food_item = selected_food.split(" - ₹")[0]
    food_cost = food_prices[food_item]
    
    if st.button("Order Food"):
        cursor.execute("SELECT booking_id FROM bookings WHERE booking_id = ?", (booking_id,))
        if cursor.fetchone():
            cursor.execute(
                "INSERT INTO food_orders (booking_id, items, total_cost) VALUES (?, ?, ?)", 
                (booking_id, food_item, food_cost)
            )
            conn.commit()
            st.success(f"Food ordered successfully! Total cost: ₹{food_cost}")
        else:
            st.error("Booking ID not found!")


def records(cursor):
    st.header("Booking Records")
    cursor.execute("SELECT * FROM bookings")
    records = cursor.fetchall()
    for record in records:
        st.markdown(f"""
        <div class="record-container">
            <div class="record-header">Booking ID: {record[0]}</div>
            <div class="record-body">
                <p><strong>Name:</strong> {record[1]}</p>
                <p><strong>Number of Guests:</strong> {record[2]}</p>
                <p><strong>Check-in Date:</strong> {record[3]}</p>
                <p><strong>Check-out Date:</strong> {record[4]}</p>
                <p><strong>Total Cost:</strong> ₹{record[5]:,.2f}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def generate_bill(cursor):
    st.header("Bill Generation/Payment")
    booking_id = st.text_input("Enter Booking ID")
    if st.button("Generate Bill"):
        cursor.execute('''
            SELECT b.name, r.room_type, b.checkin_date, b.checkout_date, b.total_cost,
                   GROUP_CONCAT(f.items), SUM(f.total_cost)
            FROM bookings b
            JOIN rooms r ON b.room_id = r.room_id
            LEFT JOIN food_orders f ON b.booking_id = f.booking_id
            WHERE b.booking_id = ?
        ''', (booking_id,))
        bill_details = cursor.fetchone()
        if bill_details:
            name, room_type, checkin_date, checkout_date, room_cost, food_items, food_cost = bill_details
            total_bill = room_cost + (food_cost if food_cost else 0)
            st.write(f"**Name:** {name}")
            st.write(f"**Room Type:** {room_type}")
            st.write(f"**Check-in:** {checkin_date}")
            st.write(f"**Check-out:** {checkout_date}")
            st.write(f"**Room Cost:** ₹{room_cost}")
            st.write(f"**Food Ordered:** {food_items if food_items else 'None'}")
            st.write(f"**Food Cost:** ₹{food_cost if food_cost else 0}")
            st.write(f"**Total Bill:** ₹{total_bill}")
        else:
            st.error("Booking ID not found!")

st.sidebar.markdown(
    """
    <style>
        .title {
            font-family: 'Arial', sans-serif;
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
            text-align: center;
            background: linear-gradient(90deg, #4b79a1, #283e51);
            padding: 10px 15px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        }
    </style>
    <div class='title'>Welcome</div>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
        menu = option_menu(
            menu_title="Navigate",  # Title for the sidebar
            options=["Room Query", "Book Room","Contact Us","About us" ,  "Check-in","Check-out" ,"Order Food","Generate Bill","Records", ],  # Menu options
            
            
            default_index=0,  # Default selected menu
            styles={
                "container": {
                    "background-color": "#1a1a1a", 
                    "padding": "10px",
                    "border-radius": "10px",
                    "box-shadow": "0 4px 10px rgba(0, 0, 0, 0.5)"
                },
                "nav-link": {
                    "font-size": "18px",
                    "color": "#00c8ff",
                    "background-color": "#333",
                    "margin": "5px",
                    "border-radius": "8px",
                    "transition": "all 0.3s ease-in-out",
                },
                "nav-link:hover": {
                    "background-color": "#00c8ff",
                    "color": "white",
                    "transform": "scale(1.05)",
                },
                "nav-link-selected": {
                    "background-color": "#005580",
                    "color": "white",
                },
            },
        )


# Call corresponding functions based on menu selection
if menu == "Room Query":
    room_query(cursor)
    
elif menu == "Book Room":
    book_room(cursor, conn)
elif menu == "Check-in":
    check_in(cursor, conn)
elif menu == "Check-out":
    check_out(cursor, conn)
elif menu == "Order Food":
    order_food(cursor, conn)
elif menu == "Generate Bill":
    generate_bill(cursor)
elif menu == "Records":
    records(cursor)
elif menu == "Contact Us":
    contact_us_page()
elif menu == "About us":
    about_us_page()
