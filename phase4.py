import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import datetime

# Connect to MySQL database
conn = mysql.connector.connect(
host='localhost', username='root', password='######', database='drone_dispatch'
# host='localhost', username='root', password='2001', database='drone_dispatch'
)
cursor = conn.cursor(buffered=True)

#Not used
def add_record(table_name):
    def submit_record():
        values = [entry.get() for entry in entries]
        if None in values:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        try:
            columns = ", ".join([col for col, val in zip(table_columns[table_name], values) if val != ""])
            placeholders = ", ".join(["%s" for val in values if val != ""])
            print(placeholders)
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, [val for val in values if val != ""])
            conn.commit()
            messagebox.showinfo("Success", "Record added successfully.")
            top.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error adding record: {err}")

    top = tk.Toplevel()
    top.title(f"Add Record to {table_name.capitalize()}")
    
    entries = []
    for i, col in enumerate(table_columns[table_name]):
        tk.Label(top, text=col.capitalize()).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(top)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    submit_button = tk.Button(top, text="Submit", command=submit_record)
    submit_button.grid(row=len(table_columns[table_name]), columnspan=2, padx=10, pady=10)

#Not used
def remove_record(table_name):
    def submit_record():
        value = entry.get()
        if not value:
            messagebox.showerror("Error", "Please enter a value.")
            return
        try:
            sql = f"DELETE FROM {table_name} WHERE uname = %s"
            cursor.execute(sql, (value,))
            conn.commit()
            messagebox.showinfo("Success", "Record removed successfully.")
            top.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error removing record: {err}")

    top = tk.Toplevel()
    top.title(f"Remove Record from {table_name.capitalize()}")

    tk.Label(top, text="Enter Username:").grid(row=0, column=0, padx=10, pady=5)
    entry = tk.Entry(top)
    entry.grid(row=0, column=1, padx=10, pady=5)

    submit_button = tk.Button(top, text="Submit", command=submit_record)
    submit_button.grid(row=1, columnspan=2, padx=10, pady=10)


#Add customer SP
def add_customer(table_name):
    
    def submit_record():
        #values = [entry.get() for entry in entries]
        values = [entry.get() if entry.get() != '' or col != 'birthdate' else None for entry, col in zip(entries, table_columns[table_name])]

        if '' or None in values[:3] or '' or None in values[5:]:
            messagebox.showerror("Error", "Please fill in all fields except birthdate(optional).")
            return
        
        if values[4]:
            try:
                datetime.datetime.strptime(values[4], "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
                return
            

            
      
        if not values[5].isdigit() or int(values[5]) <= 0 or int(values[5]) > 5:
            messagebox.showerror("Error", "Rating must be non-negative value and between 1 and 5.")
            return
        
        if not values[6].isdigit():
            messagebox.showerror("Error", "Credit must be non-negative value.")
            return

        try:
            # Check if the username already exists
            cursor.execute("SELECT COUNT(*) FROM users WHERE uname = %s", (values[0],))
            count = cursor.fetchone()[0]
            if count > 0:
                messagebox.showerror("Error", "Username already exists. Please choose a different username.")
                return

            # Call the stored procedure with the provided values
            cursor.callproc("add_customer", values)
            conn.commit()
            messagebox.showinfo("Success", "Customer added successfully.")
            top.destroy()
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            messagebox.showerror("Error", f"Error adding customer: {err}")

    top = tk.Toplevel()
    top.title(f"Add Customer")
    
    entries = []
    for i, col in enumerate(table_columns[table_name]):
        tk.Label(top, text=col.capitalize()).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(top)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    submit_button = tk.Button(top, text="Submit", command=submit_record)
    submit_button.grid(row=len(table_columns[table_name]), columnspan=2, padx=10, pady=10)
 

def increase_customer_credit(table_name):
    def submit_record():
        values = [entry.get() for entry in entries]
        if '' in values:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        uname = values[0]  
        money = values[1]
        
        # Check if money is a valid integer
        try:
            money = int(money)
        except ValueError:
            messagebox.showerror("Error", "Credit must be an integer.")
            return
        
        if money <= 0:
            messagebox.showerror("Error", "Credit must be a positive integer.")
            return
        
        try:
            # Check if the username exists in the customers table
            cursor.execute("SELECT COUNT(*) FROM customers WHERE uname = %s", (uname,))
            result = cursor.fetchone()
            if result[0] == 0:
                # Username doesn't exist, show error message
                messagebox.showerror("Error", "Username does not exist already.")
                return
            
            # Call the stored procedure with the provided values
            cursor.callproc("increase_customer_credits", values)
            conn.commit()
            messagebox.showinfo("Success", "Customer credit increased successfully.")
            top.destroy()
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            messagebox.showerror("Error", f"Error adding customer: {err}")

    top = tk.Toplevel()
    top.title(f"Increase Customer Credit")
    
    entries = []
    tk.Label(top, text="Enter uname:").grid(row=0, column=0, padx=10, pady=5)
    entry = tk.Entry(top)
    entry.grid(row=0, column=1, padx=10, pady=5)
    entries.append(entry)
    tk.Label(top, text="Enter Money:").grid(row=1, column=0, padx=10, pady=5)
    entry = tk.Entry(top)
    entry.grid(row=1, column=1, padx=10, pady=5)
    entries.append(entry)

    submit_button = tk.Button(top, text="Submit", command=submit_record)
    submit_button.grid(row=2, columnspan=2, padx=10, pady=10)

def remove_customer(table_name):
    def submit_record():
        value = entry.get()
        if not value:
            messagebox.showerror("Error", "Please enter a value.")
            return
        try:
            # Check if the customer exists
            cursor.execute("SELECT COUNT(*) FROM customers WHERE uname = %s", (value,))
            customer_count = cursor.fetchone()[0]
            if customer_count == 0:
                messagebox.showerror("Error", "Customer does not exist.")
                return
            
            # Check if the customer has pending orders
            cursor.execute("SELECT COUNT(*) FROM orders WHERE purchased_by = %s", (value,))
            order_count = cursor.fetchone()[0]
            if order_count > 0:
                messagebox.showerror("Error", "Cannot remove customer as they have pending orders.")
                return
            
            # Call the stored procedure with the provided value
            cursor.callproc("remove_customer", (value,))
            conn.commit()
            messagebox.showinfo("Success", "Customer removed successfully.")
            top.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error removing record: {err}")

    top = tk.Toplevel()
    top.title(f"Remove Customer")

    tk.Label(top, text="Enter uname:").grid(row=0, column=0, padx=10, pady=5)
    entry = tk.Entry(top)
    entry.grid(row=0, column=1, padx=10, pady=5)

    submit_button = tk.Button(top, text="Submit", command=submit_record)
    submit_button.grid(row=1, columnspan=2, padx=10, pady=10)


def add_product(table_name):
    def submit_record():
        values = [entry.get() for entry in entries]
        # Check for empty fields
        if None in values or "" in values:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        # Check if weight is negative
        try:
            weight = int(values[2])
            if weight <= 0:
                messagebox.showerror("Error", "Weight cannot be zero or negative.")
                return
        except ValueError:
            messagebox.showerror("Error", "Weight must be an integer.")
            return
        
        try:
            # Check if barcode already exists
            cursor.execute("SELECT COUNT(*) FROM products WHERE barcode = %s", (values[0],))
            count = cursor.fetchone()[0]
            if count > 0:
                messagebox.showerror("Error", "Product cannot be added as barcode already exists.")
                return

            # Call the stored procedure with the provided values
            cursor.callproc("add_product", values)
            conn.commit()
            messagebox.showinfo("Success", "Product added successfully.")
            top.destroy()
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            messagebox.showerror("Error", f"Error adding product: {err}")

    top = tk.Toplevel()
    top.title(f"Add Product")
    
    entries = []
    for i, col in enumerate(table_columns[table_name]):
        tk.Label(top, text=col.capitalize()).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(top)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    submit_button = tk.Button(top, text="Submit", command=submit_record)
    submit_button.grid(row=len(table_columns[table_name]), columnspan=2, padx=10, pady=10)

def remove_product(table_name):
    def submit_record():
        value = entry.get()

        if value == '':
            messagebox.showerror("Error", "Please enter a value.")
            return

        try:
            # Check if barcode exists in products table
            cursor.execute("SELECT * FROM products WHERE barcode = %s", (value,))
            product = cursor.fetchone()
            if not product:
                messagebox.showinfo("Invalid Barcode", "The entered barcode does not exist in the products table.")
                return

            # Consume the result before executing the next query
            cursor.fetchall()

            # Check if barcode exists in order lines table
            cursor.execute("SELECT * FROM order_lines WHERE barcode = %s", (value,))
            orderline = cursor.fetchone()
            if orderline:
                messagebox.showinfo("Product in Orderlines", "Can't remove product as it is in orderlines.")
                return

            # Consume the result before executing the next query
            cursor.fetchall()

            # Call the stored procedure with the provided value
            cursor.callproc("remove_product", [value])
            conn.commit()
            messagebox.showinfo("Success", "Product removed successfully.")
            top.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error removing product: {err}")

    top = tk.Toplevel()
    top.title("Remove Product")

    tk.Label(top, text="Enter Product Barcode:").grid(row=0, column=0, padx=10, pady=5)
    entry = tk.Entry(top)
    entry.grid(row=0, column=1, padx=10, pady=5)

    submit_button = tk.Button(top, text="Submit", command=submit_record)
    submit_button.grid(row=1, columnspan=2, padx=10, pady=10)

#Add drone SP
def add_drone(table_name):
    def submit_record():
        values = [entry.get() for entry in entries]

        # Check if any of the inputs are null or empty
        if not all(values):
            messagebox.showerror("Error", "All fields are required.")
            return

        ip_storeID, ip_droneTag, ip_capacity, ip_remaining_trips, ip_pilot = values

        # Check for datatypes and negative numbers
        try:
            ip_droneTag = int(ip_droneTag)
            ip_capacity = int(ip_capacity)
            ip_remaining_trips = int(ip_remaining_trips)
        except ValueError:
            messagebox.showerror("Error", "DroneTag, Capacity, and Remaining Trips must be integers.")
            return

        if ip_droneTag < 0 or ip_capacity < 0 or ip_remaining_trips < 0:
            messagebox.showerror("Error", "DroneTag, Capacity, and Remaining Trips must be non-negative.")
            return

        try:
            # Check if the store ID exists
            cursor.execute("SELECT COUNT(*) FROM stores WHERE storeID = %s", (ip_storeID,))
            store_exists = cursor.fetchone()[0]
            
            if store_exists != 1:
                messagebox.showerror("Error", "Invalid store ID.")
                return
            
            # Check if the drone tag is unique for the specified store
            cursor.execute("SELECT COUNT(*) FROM drones WHERE storeID = %s AND droneTag = %s", (ip_storeID, ip_droneTag))
            valid_drone = cursor.fetchone()[0]
            
            if valid_drone != 0:
                messagebox.showerror("Error", "Drone tag must be unique for the specified store.")
                return
            
            # Check if the pilot exists in the drone_pilots table
            cursor.execute("SELECT COUNT(*) FROM drone_pilots WHERE uname = %s", (ip_pilot,))
            pilot_exists = cursor.fetchone()[0]

            if pilot_exists != 1:
                messagebox.showerror("Error", "Invalid pilot name.")
                return
            
            # Check if the pilot is not currently piloting any drone
            cursor.execute("SELECT COUNT(*) FROM drones WHERE pilot = %s", (ip_pilot,))
            pilot_has_drone = cursor.fetchone()[0]
            
            if pilot_has_drone != 0:
                messagebox.showerror("Error", "The pilot is currently piloting another drone.")
                return

            # Call the stored procedure with the provided values
            cursor.callproc("add_drone", values)
            conn.commit()
            messagebox.showinfo("Success", "Drone added successfully.")
            top.destroy()
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            messagebox.showerror("Error", f"Error adding drone: {err}")

    top = tk.Toplevel()
    top.title(f"Add Drone")
    
    entries = []
    for i, col in enumerate(table_columns[table_name]):
        tk.Label(top, text=col.capitalize()).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(top)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    submit_button = tk.Button(top, text="Submit", command=submit_record)
    submit_button.grid(row=len(table_columns[table_name]), columnspan=2, padx=10, pady=10)

#Repair drone SP
def repair_drone(table_name):
    def submit_record():
        values = [entry.get() for entry in entries]
        if None in values or "" in values:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Check if refueled trips is non-negative
        refueled_trips_str = values[2]  # Assuming the refueled_trips input is the third entry
        try:
            refueled_trips = int(refueled_trips_str)
        except ValueError:
            messagebox.showerror("Error", "Refueled trips must be an integer.")
            return

        if refueled_trips < 0:
            messagebox.showerror("Error", "Refueled trips must be non-negative.")
            return

        try:
            # Validate input
            store_id = values[0]
            drone_tag = values[1]
            if not store_id or not drone_tag:
                messagebox.showerror("Error", "Please enter both StoreID and DroneTag.")
                return

            # Check if the combination of store ID and drone tag exists in the drones table
            cursor.execute("SELECT COUNT(*) FROM drones WHERE StoreID = %s AND DroneTag = %s", (store_id, drone_tag))
            combo_exists = cursor.fetchone()[0]
            if combo_exists == 0:
                messagebox.showerror("Error", "Combination of StoreID and DroneTag does not exist in the drones table.")
                return

            # Call the stored procedure with the provided values
            cursor.callproc("repair_refuel_drone", values)
            conn.commit()
            messagebox.showinfo("Success", "Drone repaired and refueled successfully.")
            top.destroy()
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            messagebox.showerror("Error", f"Error repairing and refueling drone: {err}")

    top = tk.Toplevel()
    top.title(f"Repair/Refuel Drone")
    
    entries = []
    tk.Label(top, text="Enter StoreID:").grid(row=0, column=0, padx=10, pady=5)
    entry = tk.Entry(top)
    entry.grid(row=0, column=1, padx=10, pady=5)
    entries.append(entry)
    tk.Label(top, text="Enter DroneTag:").grid(row=1, column=0, padx=10, pady=5)
    entry = tk.Entry(top)
    entry.grid(row=1, column=1, padx=10, pady=5)
    entries.append(entry)
    tk.Label(top, text="Enter refueled trips:").grid(row=2, column=0, padx=10, pady=5)
    entry = tk.Entry(top)
    entry.grid(row=2, column=1, padx=10, pady=5)
    entries.append(entry)

    submit_button = tk.Button(top, text="Submit", command=submit_record)
    submit_button.grid(row=3, columnspan=2, padx=10, pady=10)

#Remove drone SP
def remove_drone(table_name):
    def submit_record():
        values = [entry.get() for entry in entries]
        if None in values:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        try:
            # Validate input
            store_id = values[0]
            drone_tag = values[1]
            if not store_id or not drone_tag:
                messagebox.showerror("Error", "Please enter both StoreID and DroneTag.")
                return

            cursor.execute("SELECT COUNT(*) FROM stores WHERE StoreID = %s", (store_id,))
            store_exists = cursor.fetchone()[0]
            if store_exists == 0:
                messagebox.showerror("Error", "StoreID does not exist.")
                return
            
            # Check if the drone tag exists
            cursor.execute("SELECT COUNT(*) FROM drones WHERE DroneTag = %s", (drone_tag,))
            drone_exists = cursor.fetchone()[0]
            if drone_exists == 0:
                messagebox.showerror("Error", "DroneTag does not exist.")
                return
            
            # Check if the drone with the given StoreID and DroneTag combination exists
            cursor.execute("SELECT COUNT(*) FROM drones WHERE StoreID = %s AND DroneTag = %s", (store_id, drone_tag))
            drone_store_combo_exists = cursor.fetchone()[0]
            if drone_store_combo_exists == 0:
                messagebox.showerror("Error", "Drone with the entered StoreID and DroneTag combination does not exist.")
                return
                
            # Check if the drone is carrying any pending orders
            cursor.execute("SELECT COUNT(*) FROM orders WHERE carrier_store = %s AND carrier_tag = %s", (store_id, drone_tag))
            pending_orders = cursor.fetchone()[0]
            if pending_orders > 0:
                messagebox.showerror("Error", "Cannot remove drone. It is carrying pending orders.")
                return
            
            # Call the stored procedure with the provided values
            cursor.callproc("remove_drone", values)
            conn.commit()
            messagebox.showinfo("Success", "Drone removed successfully.")
            top.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error removing drone: {err}")

    top = tk.Toplevel()
    top.title(f"Remove Drone")

    entries = []
    tk.Label(top, text="Enter StoreID:").grid(row=0, column=0, padx=10, pady=5)
    entry = tk.Entry(top)
    entry.grid(row=0, column=1, padx=10, pady=5)
    entries.append(entry)
    tk.Label(top, text="Enter DroneTag:").grid(row=1, column=0, padx=10, pady=5)
    entry = tk.Entry(top)
    entry.grid(row=1, column=1, padx=10, pady=5)
    entries.append(entry)

    submit_button = tk.Button(top, text="Submit", command=submit_record)
    submit_button.grid(row=2, columnspan=2, padx=10, pady=10)

#Add drone pilot SP
def add_drone_pilot(table_name):
    def submit_record():
        values = [entry.get() for entry in entries]
        
        # Check for empty fields
        if None in values or "" in values:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        #check int data type
        if not values[6].isdigit():
            messagebox.showerror("Error", "Service must be non-negative number.")
            return
        
        if not values[7].isdigit():
            messagebox.showerror("Error", "Salary must be non-negative number.")
            return
        
        if not values[9].isdigit():
            messagebox.showerror("Error", "Experience must be non-negative number.")
            return

        # Check if date is in valid format
        try:
            datetime.datetime.strptime(values[4], "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return
        
        #negative value check for service, salary and exp
        if int(values[6]) <= 0 or int(values[7]) <= 0 or int(values[9]) < 0:
            messagebox.showerror("Error", "Invalid service or salary or experience")
            return
        
        #Check if uname exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE uname = %s", (values[0],))
        pilot_exists = cursor.fetchone()[0]
        if pilot_exists != 0:
            messagebox.showerror("Error", "Pilot with that username already exists.")
            return
        
        #Check if taxID exists
        cursor.execute("SELECT COUNT(*) FROM employees WHERE taxID = %s", (values[5],))
        taxid_exists = cursor.fetchone()[0]
        if taxid_exists != 0:
            messagebox.showerror("Error", "Pilot with that taxID already exists.")
            return
        
        #Check if licenseID exists
        cursor.execute("SELECT COUNT(*) FROM drone_pilots WHERE licenseID = %s", (values[8],))
        license_exists = cursor.fetchone()[0]
        if license_exists != 0:
            messagebox.showerror("Error", "Pilot with that licenseID already exists.")
            return

        try:
            # Call the stored procedure with the provided values
            cursor.callproc("add_drone_pilot", values)
            conn.commit()
            messagebox.showinfo("Success", "Drone pilot added successfully.")
            top.destroy()
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            messagebox.showerror("Error", f"Error adding drone: {err}")

    top = tk.Toplevel()
    top.title(f"Add Drone Pilot")
    
    entries = []
    for i, col in enumerate(table_columns[table_name]):
        tk.Label(top, text=col.capitalize()).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(top)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    submit_button = tk.Button(top, text="Submit", command=submit_record)
    submit_button.grid(row=len(table_columns[table_name]), columnspan=2, padx=10, pady=10)

#swap drone control SP
def swap_drone_control(table_name):
    # Function to check pilot existence
    def check_pilot_existence(pilot):
        try:
            cursor.execute("SELECT COUNT(*) FROM drone_pilots WHERE uname = %s", (pilot,))
            pilot_count = cursor.fetchone()[0]
            return pilot_count == 1
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error checking pilot existence: {err}")
            return False

    def submit_record():
        incoming_pilot = incoming_pilot_entry.get()
        outgoing_pilot = outgoing_pilot_entry.get()
        
        # Check if both pilots are provided
        if not incoming_pilot or not outgoing_pilot:
            messagebox.showerror("Error", "Both incoming and outgoing pilots must be provided.")
            return
        
        # Check data type for incoming pilot
        if not isinstance(incoming_pilot, str):
            messagebox.showerror("Error", "Incoming pilot must be a string.")
            return
        
        # Check data type for outgoing pilot
        if not isinstance(outgoing_pilot, str):
            messagebox.showerror("Error", "Outgoing pilot must be a string.")
            return
        
        # Check if incoming pilot is a valid pilot and exists in the drone table
        if not check_pilot_existence(incoming_pilot):
            messagebox.showerror("Error", "Incoming pilot is not a valid pilot.")
            return

        # Check if outgoing pilot is a valid pilot and exists in the drone table
        if not check_pilot_existence(outgoing_pilot):
            messagebox.showerror("Error", "Outgoing pilot is not a valid pilot.")
            return
        
        try:
            # Check if the incoming pilot exists in the drone table
            cursor.execute("SELECT COUNT(*) FROM drones WHERE pilot = %s", (incoming_pilot,))
            incoming_pilot_count = cursor.fetchone()[0]
            if incoming_pilot_count != 0:
                messagebox.showerror("Error", "Incoming pilot is currently controlling a drone.")
                return

            # Check if the outgoing pilot exists in the drone table
            cursor.execute("SELECT COUNT(*) FROM drones WHERE pilot = %s", (outgoing_pilot,))
            outgoing_pilot_count = cursor.fetchone()[0]
            if outgoing_pilot_count != 1:
                messagebox.showerror("Error", "Outgoing pilot is not currently controlling a drone.")
                return

            # Call the stored procedure with the provided values
            cursor.callproc("swap_drone_control", (incoming_pilot, outgoing_pilot))
            conn.commit()
            messagebox.showinfo("Success", "Drone pilots swapped successfully.")
            top.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error swapping drone pilots: {err}")

    top = tk.Toplevel()
    top.title("Swap Drone Control")

    incoming_pilot_label = tk.Label(top, text="Incoming Pilot:")
    incoming_pilot_label.grid(row=0, column=0, padx=10, pady=5)
    incoming_pilot_entry = tk.Entry(top)
    incoming_pilot_entry.grid(row=0, column=1, padx=10, pady=5)

    outgoing_pilot_label = tk.Label(top, text="Outgoing Pilot:")
    outgoing_pilot_label.grid(row=1, column=0, padx=10, pady=5)
    outgoing_pilot_entry = tk.Entry(top)
    outgoing_pilot_entry.grid(row=1, column=1, padx=10, pady=5)

    submit_button = tk.Button(top, text="Submit", command=submit_record)
    submit_button.grid(row=2, columnspan=2, padx=10, pady=10)

#Remove drone pilot SP
def remove_drone_pilot(table_name):
    def submit_record():
        value = entry.get()
        if not value:
            messagebox.showerror("Error", "Please enter a value.")
            return
        
        try:
            # Check if the pilot exists in the pilots table
            cursor.execute("SELECT COUNT(*) FROM drone_pilots WHERE uname = %s", (value,))
            pilot_count = cursor.fetchone()[0]
            if pilot_count != 1:
                messagebox.showerror("Error", "Pilot does not exist.")
                return

            # Check if the pilot is controlling a drone
            cursor.execute("SELECT COUNT(*) FROM drones WHERE pilot = %s", (value,))
            pilot_count = cursor.fetchone()[0]
            if pilot_count != 0:
                messagebox.showerror("Error", "Cannot remove pilot. Pilot is currently controlling a drone.")
                return

            cursor.callproc("remove_drone_pilot", (value,))
            conn.commit()
            messagebox.showinfo("Success", "Drone pilot removed successfully.")
            top.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error removing drone pilot: {err}")

    top = tk.Toplevel()
    top.title(f"Remove Drone Pilot")

    tk.Label(top, text="Enter uname:").grid(row=0, column=0, padx=10, pady=5)
    entry = tk.Entry(top)
    entry.grid(row=0, column=1, padx=10, pady=5)

    submit_button = tk.Button(top, text="Submit", command=submit_record)
    submit_button.grid(row=1, columnspan=2, padx=10, pady=10)

#Begin order SP
def begin_order(table_name):
    def submit_record():
 
        values = [entry.get() for entry in entries]

        # Check for empty fields
        if None in values or "" in values:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        #negative value check for quantity and price
        if int(values[6]) <= 0 or int(values[7]) <= 0:
            messagebox.showerror("Error", "Invalid quantity or price")
            return

        # Check if date is in valid format
        try:
            datetime.datetime.strptime(values[1], "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        # Check if customer exists in the customers table
        cursor.execute("SELECT COUNT(*) FROM customers WHERE uname = %s", (values[2],))
        customer_exists = cursor.fetchone()[0]
        if customer_exists == 0:
            messagebox.showerror("Error", "Customer does not exist.")
            return
        
        # Check if order does not exist table
        cursor.execute("SELECT COUNT(*) FROM orders WHERE orderid = %s", (values[0],))
        orderid_not_exists = cursor.fetchone()[0]
        if orderid_not_exists != 0:
            messagebox.showerror("Error", "OrderID already exists.")
            return
        
        #check valid barcode
        cursor.execute("SELECT COUNT(*) FROM products WHERE barcode = %s", (values[5],))
        product_exists = cursor.fetchone()[0]
        if product_exists == 0:
            messagebox.showerror("Error", "Product does not exist.")
            return
        
        #check valid drone
        cursor.execute("select COUNT(*) from drones where concat(storeID, droneTag) LIKE concat(%s, %s)", (values[3],values[4],))
        drone_exists = cursor.fetchone()[0]
        if drone_exists == 0:
            messagebox.showerror("Error", "Drone does not exist.")
            return
        
        #check enough credits
        #cursor.execute("select sum(price* quantity) from orders natural join order_lines where orderID = %s group by purchased_by", (values[0],))
        #current_order_value = cursor.fetchone()[0]
        cursor.execute("select credit from customers where uname LIKE %s", (values[2],))
        remaining_credit = cursor.fetchone()[0]
        if (int(values[6])*int(values[7])) > remaining_credit:
            messagebox.showerror("Error", "Not enough credits.")
            return
        
        cursor.execute("select capacity from drones where concat(storeID, droneTag) LIKE concat(%s, %s)", (values[3],values[4],))
        rem_capacity = cursor.fetchone()[0]
        cursor.execute("select weight from products where barcode = %s", (values[5],))
        prod_weight = cursor.fetchone()[0]
        if rem_capacity < (int(values[7]) * prod_weight):
            messagebox.showerror("Error", "Not enough lifting capacity.")
            return
        
 
        try:
            # Call the stored procedure with the provided values
            cursor.callproc("begin_order", values)
            conn.commit()
            messagebox.showinfo("Success", "New Order created successfully.")
            top.destroy()
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            messagebox.showerror("Error", f"Error creating order: {err}")

    top = tk.Toplevel()
    top.title(f"Begin Order")

    entries = []
    for i, col in enumerate(table_columns[table_name]):
        tk.Label(top, text=col.capitalize()).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(top)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    submit_button = tk.Button(top, text="Submit", command=submit_record)
    submit_button.grid(row=len(table_columns[table_name]), columnspan=2, padx=10, pady=10)

#Add order line SP
def add_order_line(table_name):
    def submit_record():
        values = [entry.get() for entry in entries]
        
        # Check for empty fields
        if None in values or "" in values:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        #negative value check for quantity and price
        if int(values[2]) <= 0 or int(values[3]) <= 0:
            messagebox.showerror("Error", "Invalid quantity or price")
            return
        
        #check int data type
        if not values[2].isdigit():
            messagebox.showerror("Error", "Quantity must be non-negative number.")
            return
        
        if not values[3].isdigit():
            messagebox.showerror("Error", "Price must be non-negative number.")
            return
        
        #check if order exists in orders table
        cursor.execute("SELECT COUNT(*) FROM orders WHERE orderid = %s", (values[0],))
        orderid_not_exists = cursor.fetchone()[0]
        if orderid_not_exists == 0:
            messagebox.showerror("Error", "OrderID does not exist.")
            return
        
        #check valid product 
        cursor.execute("SELECT COUNT(*) FROM products WHERE barcode = %s", (values[1],))
        product_exists = cursor.fetchone()[0]
        if product_exists == 0:
            messagebox.showerror("Error", "Invalid product.")
            return
        
        #check duplicate product 
        cursor.execute("select COUNT(*) from order_lines where orderID = %s and barcode = %s", (values[0], values[1],))
        dup_barcode = cursor.fetchone()[0]
        if dup_barcode != 0:
            messagebox.showerror("Error", "Product already exists.")
            return
        
        #check enough credits
        cursor.execute("select sum(price* quantity) from orders natural join order_lines where orderID = %s group by orderID", (values[0],))
        current_order_value = cursor.fetchone()[0]
        cursor.execute("select credit from orders join customers on purchased_by = uname where orderID LIKE %s", (values[0],))
        remaining_credit = cursor.fetchone()[0]
        if (current_order_value + int(values[2])*int(values[3])) > remaining_credit:
            messagebox.showerror("Error", "Not enough credits.")
            return
        
        #check enough lifting capacity
        cursor.execute("select SUM(ol.quantity * p.weight) from order_lines ol \
	            join orders o on ol.orderID = o.orderID join products p on ol.barcode = p.barcode join drones on concat(storeID, droneTag) = concat(o.carrier_store, o.carrier_tag) \
                where o.orderID = %s group by o.orderID", (values[0],))
        total_current_weight = cursor.fetchone()[0]
        cursor.execute("select capacity from drones join orders on concat(storeID, droneTag) = concat(carrier_store, carrier_tag) where orderID = %s", (values[0],))
        rem_capacity = cursor.fetchone()[0]
        cursor.execute("select weight from products where barcode = %s", (values[1],))
        prod_weight = cursor.fetchone()[0]
        if rem_capacity < (int(values[3]) * prod_weight) + total_current_weight:
            messagebox.showerror("Error", "Not enough lifting capacity.")
            return

        try:
            # Call the stored procedure with the provided values
            cursor.callproc("add_order_line", values)
            conn.commit()
            messagebox.showinfo("Success", "New product added successfully.")
            top.destroy()
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            messagebox.showerror("Error", f"Error adding product: {err}")

    top = tk.Toplevel()
    top.title(f"Add product")
    
    entries = []
    for i, col in enumerate(table_columns[table_name]):
        if col in ["sold_on", "purchased_by", "carrier_store", "carrier_tag"]:
            continue
        else:
            tk.Label(top, text=col.capitalize()).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(top)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

    submit_button = tk.Button(top, text="Submit", command=submit_record)
    submit_button.grid(row=len(table_columns[table_name]), columnspan=2, padx=10, pady=10)

#Deliver Order SP
def deliver_order(table_name):
    def submit_record():
        values = [entry.get()]

        # Check for empty fields
        if None in values or "" in values:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        #check if order exists in orders table
        cursor.execute("SELECT COUNT(*) FROM orders WHERE orderid = %s", (values[0],))
        orderid_not_exists = cursor.fetchone()[0]
        if orderid_not_exists == 0:
            messagebox.showerror("Error", "OrderID does not exist.")
            return
        
        #check remaining trips
        cursor.execute("select remaining_trips from drones join drone_pilots on pilot=uname where concat(storeID, droneTag) \
                       in (select concat(carrier_store, carrier_tag) as drone_tag_tmp from orders where orderID = %s)", (values[0],))
        rem_trips = cursor.fetchone()[0]
        if rem_trips <= 0:
            messagebox.showerror("Error", "Drone needs to be repaired or refueled.")
            return
        
        try:
            # Call the stored procedure with the provided values
            cursor.callproc("deliver_order", values)
            conn.commit()
            messagebox.showinfo("Success", "Order placed successfully.")
            top.destroy()
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            messagebox.showerror("Error", f"Error adding product: {err}")

    top = tk.Toplevel()
    top.title(f"Confirm Order")
    
    tk.Label(top, text="Enter OrderID:").grid(row=0, column=0, padx=10, pady=5)
    entry = tk.Entry(top)
    entry.grid(row=0, column=1, padx=10, pady=5)

    submit_button = tk.Button(top, text="Submit", command=submit_record)
    submit_button.grid(row=2, columnspan=2, padx=10, pady=10)

#Cancel Order SP
def cancel_order(table_name):
    def submit_record():
        values = [entry.get()]
        
        # Check for empty fields
        if None in values or "" in values:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        #check if order exists in orders table
        cursor.execute("SELECT COUNT(*) FROM orders WHERE orderid = %s", (values[0],))
        orderid_not_exists = cursor.fetchone()[0]
        if orderid_not_exists == 0:
            messagebox.showerror("Error", "OrderID does not exist.")
            return
        
        try:
            # Call the stored procedure with the provided values
            cursor.callproc("cancel_order", values)
            conn.commit()
            messagebox.showinfo("Success", "Order canceled successfully.")
            top.destroy()
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            messagebox.showerror("Error", f"Error canceling order: {err}")

    top = tk.Toplevel()
    top.title(f"Cancel Order")
    
    tk.Label(top, text="Enter OrderID:").grid(row=0, column=0, padx=10, pady=5)
    entry = tk.Entry(top)
    entry.grid(row=0, column=1, padx=10, pady=5)

    submit_button = tk.Button(top, text="Submit", command=submit_record)
    submit_button.grid(row=2, columnspan=2, padx=10, pady=10)


# Function to display view in a table format
def display_view(view_name):
    top = tk.Toplevel()
    top.title(view_name.capitalize())
    
    # Fetch data from the view
    cursor.execute(f"SELECT * FROM {view_name}")
    rows = cursor.fetchall()

    # Create table to display view
    tree = ttk.Treeview(top)
    tree["columns"] = tuple(range(len(rows[0])))
    tree["show"] = "headings"

    # Add column headings
    for i, col in enumerate(cursor.description):
        tree.heading(i, text=col[0])

    # Add rows
    for row in rows:
        tree.insert("", "end", values=row)

    tree.pack(fill="both", expand=True)

# Create main window
root = tk.Tk()
root.title("Drone Dispatch")
root.geometry( "600x300" ) 

# Define table columns
table_columns = {
    "customers": ["uname", "first_name", "last_name", "address", "birthdate", "rating", "credit"],
    "products": ["barcode", "pname", "weight"],
    "drones": ["storeID", "droneTag", "capacity", "remaining_trips", "pilot"],
    "drone_pilots": ["uname", "first_name", "last_name", "address", "birthdate", "taxID", "service", "salary", "licenseID", "experience"],
    "orders": ["orderID", "sold_on", "purchased_by", "carrier_store", "carrier_tag", "barcode", "price", "quantity"],
    "views": ["most_popular_products", "drone_traffic_control", "drone_pilot_roster", "store_sales_overview", "role_distribution", "customer_credit_check", "orders_in_progress"]
}

# Create buttons with OptionMenus
for i, table_name in enumerate(table_columns.keys()):
    tk.Label(root, text=table_name.capitalize()).grid(row=i, column=0, padx=10, pady=5)
    
    if table_name == "customers":
    # Create OptionMenu with Add and Remove options
        option_var = tk.StringVar(root)
        option_var.set("Select Action")
        option_menu = tk.OptionMenu(root, option_var, "Add Customer", "Increase Customer Credit", "Remove Customer", command=lambda choice, name=table_name: customer_operation(choice, name))
        option_menu.grid(row=i, column=1, padx=10, pady=5)

    elif table_name == "products":
    # Create OptionMenu with Add and Remove options
        option_var = tk.StringVar(root)
        option_var.set("Select Action")
        option_menu = tk.OptionMenu(root, option_var, "Add Product", "Remove Product", command=lambda choice, name=table_name: product_operation(choice, name))
        option_menu.grid(row=i, column=1, padx=10, pady=5)

    elif table_name == "drones":
    # Create OptionMenu with Add and Remove options
        option_var = tk.StringVar(root)
        option_var.set("Select Action")
        option_menu = tk.OptionMenu(root, option_var, "Add Drone", "Repair/Refuel Drone", "Remove Drone", command=lambda choice, name=table_name: drone_operation(choice, name))
        option_menu.grid(row=i, column=1, padx=10, pady=5)

    elif table_name == "drone_pilots":
    # Create OptionMenu with Add and Remove options
        option_var = tk.StringVar(root)
        option_var.set("Select Action")
        option_menu = tk.OptionMenu(root, option_var, "Add Drone Pilot", "Swap Drone Control", "Remove Drone Pilot", command=lambda choice, name=table_name: drone_pilot_operation(choice, name))
        option_menu.grid(row=i, column=1, padx=10, pady=5)

    elif table_name == "orders":
        option_var = tk.StringVar(root)
        option_var.set("Select Action")
        option_menu = tk.OptionMenu(root, option_var, "Begin Order", "Add Order Line", "Deliver Order", "Cancel Order", command=lambda choice, name=table_name: order_operation(choice, name))
        option_menu.grid(row=i, column=1, padx=10, pady=5)

    elif table_name == "views":
        option_var = tk.StringVar(root)
        option_var.set("Select Action")
        option_menu = tk.OptionMenu(root, option_var, "most_popular_products", "drone_traffic_control", "drone_pilot_roster", "store_sales_overview", "role_distribution", "customer_credit_check", "orders_in_progress", command=lambda choice, name=table_name: views(choice, name))
        option_menu.grid(row=i, column=1, padx=10, pady=5)

# Function to handle OptionMenu selection
def views(choice, table_name):
    if choice == "most_popular_products":
        display_view("most_popular_products")
    elif choice == "drone_traffic_control":
        display_view("drone_traffic_control")
    elif choice == "drone_pilot_roster":
        display_view("drone_pilot_roster")
    elif choice == "store_sales_overview":
        display_view("store_sales_overview")
    elif choice == "role_distribution":
        display_view("role_distribution")
    elif choice == "customer_credit_check":
        display_view("customer_credit_check")
    elif choice == "orders_in_progress":
        display_view("orders_in_progress")

def customer_operation(choice, table_name):
    if choice == "Add Customer":
        add_customer(table_name)
    elif choice == "Increase Customer Credit":
        increase_customer_credit(table_name)
    elif choice == "Remove Customer":
        remove_customer(table_name)

def product_operation(choice, table_name):
    if choice == "Add Product":
        add_product(table_name)
    elif choice == "Remove Product":
        remove_product(table_name)

def drone_operation(choice, table_name):
    if choice == "Add Drone":
        add_drone(table_name)
    elif choice == "Repair/Refuel Drone":
        repair_drone(table_name)
    elif choice == "Remove Drone":
        remove_drone(table_name)

def drone_pilot_operation(choice, table_name):
    if choice == "Add Drone Pilot":
        add_drone_pilot(table_name)
    elif choice == "Remove Drone Pilot":
        remove_drone_pilot(table_name)
    elif choice == "Swap Drone Control":
        swap_drone_control(table_name)

def order_operation(choice, table_name):
    if choice == "Begin Order":
        begin_order(table_name)
    elif choice == "Add Order Line":
        add_order_line(table_name)
    elif choice == "Deliver Order":
        deliver_order(table_name)
    elif choice == "Cancel Order":
        cancel_order(table_name)

root.mainloop()
