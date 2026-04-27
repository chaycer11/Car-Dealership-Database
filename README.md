# Car-Dealership-Database | Chayce Merchant


# WKU Auto Group - Car Dealership Management System

**Course:** CS351 – Database Management Systems  
**Term Project**

## Project Overview
The WKU Auto Group application is a full-stack, role-based database management system designed to simulate the operations of a real-world car dealership. It provides a secure web interface for customers to browse available inventory, and for dealership employees to manage sales, service repairs, customer data, and operational reporting.

## Key Features & Role-Based Access
This application implements strict Role-Based Access Control (RBAC) to ensure users only see what they are authorized to use.

* **Customers & Guests:** Can view available vehicle inventory, use advanced search filters (make, model, year, max price), and register for an account.
* **Salespeople:** Can add new vehicles to the inventory, assign vehicle locations (e.g., Main Lot, In Transit), process vehicle sales (updating status to 'sold'), and query the customer database.
* **Mechanics:** Have access to a dedicated Service Queue showing only vehicles currently in maintenance. They can log new service tickets, assign mechanics, input mileage, and record work performed.
* **Billing Staff:** Can process customer payments for both vehicle sales and service repairs.
* **Management Dashboard:** A live operational dashboard that generates real-time reports using SQL aggregate functions (e.g., Total Vehicles Sold, Cars in Service Bay, Total Asset Value).

## Technology Stack
* **Backend:** Python 3, Flask framework
* **Database:** MySQL
* **Frontend:** HTML5, Jinja2 Templating, Bootstrap 5 (CSS/JS)
* **Authentication:** Flask-Login, Werkzeug Security (Scrypt password hashing)
* **Forms:** Flask-WTF

---

## Installation & Setup Instructions

Follow these steps to reproduce the project results and run the application locally.

### Prerequisites
* Python 3.8+ installed
* MySQL Server installed and running

### Step 1: Database Setup
1. Open your MySQL client (e.g., MySQL Workbench or command line).
2. Execute the provided `schema.sql` file. This will automatically:
   * Create the `car_dealership` database.
   * Generate all necessary tables (`Employee`, `Vehicle`, `Customer`, `Billing`, `Sale`, `Service`).
3. *(Optional)* Insert sample data into the database to test the application.

### Step 2: Environment Configuration
Create a file named `.env` in the root directory of the project. Add your local MySQL database credentials to this file:

```text
DB_HOST=localhost
DB_USER=root
DB_PASS=your_mysql_password
DB_NAME=car_dealership
DB_PORT=3306