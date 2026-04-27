import mysql.connector
import os
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASS'),
        database=os.environ.get('DB_NAME'),
        port=os.environ.get('DB_PORT')
    )
    return connection

def get_all_inventory(make=None, model=None, year=None, max_price=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM Vehicle WHERE 1=1" 
    params = []

    if make:
        query += " AND make LIKE %s"
        params.append(f"%{make}%")
    if model:
        query += " AND model LIKE %s"
        params.append(f"%{model}%")
    if year:
        query += " AND year = %s"
        params.append(year)
    if max_price:
        query += " AND price <= %s"
        params.append(max_price)

    cursor.execute(query, tuple(params))
    vehicles = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return vehicles

def get_selected_vehicles(query):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(query)
    vehicles = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return vehicles

def insert_vehicle(vin, make, model, year, price, location):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # We automatically set status to 'inventory' and location to 'main_lot'
        cursor.execute(
            "INSERT INTO Vehicle (vin, make, model, year, price, status, location) VALUES (%s, %s, %s, %s, %s, 'available', %s)",
            (vin, make, model, year, price, location)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Failed to insert vehicle: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def insert_customer(name, email, phone, address, customer_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Customer (name, email, phone, address, customer_type) VALUES (%s, %s, %s, %s, %s)",
            (name, email, phone, address, customer_type)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Failed to insert customer: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def process_sale(vehicle_id, customer_id, temp_tag_num, customization_work="None", salesperson_id=1):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 1. Create the Sale Record
        # (Note: billing_id is left NULL for now just like your ER diagram allows)
        cursor.execute(
            """INSERT INTO Sale (sale_date, temp_tag_num, customization_work, customer_id, vehicle_id, salesperson_id) 
               VALUES (CURDATE(), %s, %s, %s, %s, %s)""",
            (temp_tag_num, customization_work, customer_id, vehicle_id, salesperson_id)
        )

        # 2. Update the Vehicle Status
        cursor.execute(
            "UPDATE Vehicle SET status = 'sold' WHERE vehicle_id = %s",
            (vehicle_id,)
        )

        # 3. If BOTH succeed, we commit the changes to Aiven
        conn.commit()
        return True
    
    except Exception as e:
        print(f"Failed to process sale: {e}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()


def process_service(vehicle_id, customer_id, mechanic_id, mileage_in, mileage_out, estimate, work_done):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
       
        cursor.execute(
            """INSERT INTO Service (preliminary_estimate, work_done, 
                                    mileage_in, mileage_out, vehicle_id, customer_id) 
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (estimate, work_done, mileage_in, mileage_out, vehicle_id, customer_id)
        )
        
        new_service_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO Service_Assignment (service_id, mechanic_id) VALUES (%s, %s)",
            (new_service_id, mechanic_id)
        )

        conn.commit()
        return True
    
    except Exception as e:
        print(f"Failed to process service: {e}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()

def get_mechanics():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # We only want the ID and the Name of people who are mechanics
        cursor.execute("SELECT employee_id, name FROM Employee WHERE role = 'mechanic'")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching mechanics: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def process_payment(ticket_type, ticket_id, amount, payment_method):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 1. Create the Billing Record
        cursor.execute(
            """INSERT INTO Billing (billing_date, amount, payment_method) 
               VALUES (CURDATE(), %s, %s)""",
            (amount, payment_method)
        )
        
        # Grab the newly created billing_id
        new_billing_id = cursor.lastrowid

        # 2. Update the correct table to link the payment
        if ticket_type == 'sale':
            cursor.execute(
                "UPDATE Sale SET billing_id = %s WHERE sale_id = %s",
                (new_billing_id, ticket_id)
            )
        elif ticket_type == 'service':
            cursor.execute(
                "UPDATE Service SET billing_id = %s WHERE service_id = %s",
                (new_billing_id, ticket_id)
            )

        # 3. Commit the transaction
        conn.commit()
        return True
    
    except Exception as e:
        print(f"Failed to process payment: {e}")
        conn.rollback() 
        return False
    finally:
        cursor.close()
        conn.close()


def authenticate_user(email, password, user_type):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    table = "Employee" if user_type == 'employee' else "Customer"
    id_col = "employee_id" if user_type == 'employee' else "customer_id"
    
    cursor.execute(f"SELECT * FROM {table} WHERE email = %s", (email,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row and check_password_hash(row['password'], password):
        # We prefix the ID so the user_loader knows which table to check later
        session_id = f"{user_type[0:3]}_{row[id_col]}" # e.g., 'emp_1'
        role = row.get('role', 'customer')
        return User(id=session_id, name=row['name'], role=role, user_type=user_type)
    return None

def create_customer(name, phone, email, address, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pw = generate_password_hash(password) # SALT AND HASH
    try:
        cursor.execute(
            "INSERT INTO Customer (name, phone, email, address, password) VALUES (%s, %s, %s, %s, %s)",
            (name, phone, email, address, hashed_pw)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Registration Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_user_by_id(session_id):
    # This is for Flask-Login to remember the user between page clicks
    prefix, uid = session_id.split('_')
    table = "Employee" if prefix == 'emp' else "Customer"
    id_col = "employee_id" if prefix == 'emp' else "customer_id"
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table} WHERE {id_col} = %s", (uid,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        return User(id=session_id, name=row['name'], role=row.get('role', 'customer'), user_type=table.lower())
    return None



def get_showroom_vehicles(make=None, model=None, year=None, max_price=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Base query: ALWAYS filter out sold/maintenance cars
    query = "SELECT * FROM Vehicle WHERE status = 'available'"
    params = [] 

    if make:
        query += " AND make LIKE %s"
        params.append(f"%{make}%") 
    if model:
        query += " AND model LIKE %s"
        params.append(f"%{model}%")
    if year:
        query += " AND year = %s"
        params.append(year)
    if max_price:
        query += " AND price <= %s"
        params.append(max_price)

    # Execute securely
    cursor.execute(query, tuple(params))
    vehicles = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return vehicles

def get_service_queue():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Only fetch cars that are in the shop
    query = "SELECT * FROM Vehicle WHERE status = 'maintenance'"
    cursor.execute(query)
    vehicles = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return vehicles

def search_customers(search_term):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    
    query = """
        SELECT * FROM Customer 
        WHERE name LIKE %s 
           OR email LIKE %s 
           OR phone LIKE %s
    """
    
    # Format the search term for SQL wildcard matching
    formatted_term = f"%{search_term}%"
    
    # Pass the formatted term three times (once for name, email, and phone)
    cursor.execute(query, (formatted_term, formatted_term, formatted_term))
    customers = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return customers

def get_operational_report():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    stats = {}

    try:
        # 1. Total Available Inventory & Value
        cursor.execute("SELECT COUNT(*) as count, SUM(price) as total_value FROM Vehicle WHERE status = 'available'")
        inventory = cursor.fetchone()
        stats['inventory_count'] = inventory['count'] or 0
        stats['inventory_value'] = inventory['total_value'] or 0

        # 2. Total Vehicles Sold
        cursor.execute("SELECT COUNT(*) as count FROM Vehicle WHERE status = 'sold'")
        sold = cursor.fetchone()
        stats['sold_count'] = sold['count'] or 0

        # 3. Vehicles in the Service Bay
        cursor.execute("SELECT COUNT(*) as count FROM Vehicle WHERE status = 'maintenance'")
        service = cursor.fetchone()
        stats['service_count'] = service['count'] or 0

    except Exception as e:
        print(f"Error generating report: {e}")
        
    finally:
        cursor.close()
        conn.close()
        
    return stats