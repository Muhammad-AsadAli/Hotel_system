from flask import Flask, render_template, request, jsonify
import psycopg2
from psycopg2 import IntegrityError

app = Flask(__name__)

class Database:
    def __init__(self):
        # Establish a connection to the PostgreSQL database
        self.conn = psycopg2.connect(
            dbname="",        
            user="",        
            password="",
            host="",       
            port=""              
        )
        self.create_tables() 

    def create_tables(self):
        if not hasattr(self, 'conn'):
            print("Database connection is not established.")
            return

        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS customer_data (
                    name VARCHAR(255) PRIMARY KEY,
                    address VARCHAR(255) NOT NULL,
                    checkin  DATE NOT NULL,
                    checkout  DATE NOT NULL,
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS room_rent (
                    id SERIAL PRIMARY KEY,
                    room_type VARCHAR(255),
                    number_night VARCHAR(255),

                )
            """)
            self.conn.commit()
            print("Tables created successfully.")

    def insert_user(self, name, address, checkin, checkout):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (name, address, checkin, checkout) VALUES (%s, %s, %s,%s)",
                (name, address, checkin, checkout)
            )
        self.conn.commit()

    def insert_attendance(self, room_type, number_night):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO attendance (room_type, number_night) VALUES (%s, %s)",
                (room_type, number_night)
            )
        self.conn.commit()

    # def close_connection(self):
    #     if self.conn:
    #         self.conn.close()
    #         print("Database connection closed.")

db = Database()

# Store customer data and total costs
customer_data = {}
room_rent = 0
additional_charges = 1800

# Route for homepage
app= Flask(__name__,template_folder='template')
@app.route('/')
def home():
    return render_template('index.html')

# Route for submitting customer data
@app.route('/submit_customer_data', methods=['POST'])
def submit_customer_data():
    global customer_data
    customer_data = {
        'name': request.form['name'],
        'address': request.form['address'],
        'cindate': request.form['cindate'],
        'coutdate': request.form['coutdate']
    }
    return jsonify(success=True, message="Customer data submitted successfully.")

# Route for calculating room rent
@app.route('/calculate_room_rent', methods=['POST'])
def calculate_room_rent():
    global room_rent
    room_type = request.form['room_type']
    nights = int(request.form['nights'])

    rates = {'A': 6000, 'B': 5000, 'C': 4000, 'D': 3000}
    room_rent = rates[room_type] * nights

    return jsonify(success=True, room_rent=room_rent)

# Route for displaying the total cost
@app.route('/show_total_cost', methods=['GET'])
def show_total_cost():
    global customer_data, room_rent, additional_charges
    if not customer_data:
        return jsonify(success=False, message="Please submit customer data first.")

    total_cost = room_rent + additional_charges
    return jsonify(
        success=True,
        customer_data=customer_data,
        room_rent=room_rent,
        additional_charges=additional_charges,
        total_cost=total_cost
    )

if __name__ == '__main__':
    app.run(debug=True)
