-- 1. Create the database
CREATE DATABASE IF NOT EXISTS car_dealership;
USE car_dealership;

-- 2. Create Independent Tables (No Foreign Keys yet)
CREATE TABLE VEHICLE (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    vin VARCHAR(17) UNIQUE NOT NULL,
    make VARCHAR(50),
    model VARCHAR(50),
    year INT,
    price DECIMAL(10, 2),
    status ENUM('inventory', 'sold', 'leased', 'in_service'),
    location ENUM('main_lot', 'remote_lot', 'other_dealership', 'in_transit')
);

CREATE TABLE CUSTOMER (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    phone_number VARCHAR(20),
    email VARCHAR(100),
    customer_type ENUM('purchase', 'service', 'visit')
);

CREATE TABLE EMPLOYEE (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    phone_number VARCHAR(20),
    email VARCHAR(100),
    role ENUM('mechanic', 'salesperson', 'billing')
);

-- 3. Create Dependent Tables (These use Foreign Keys)
CREATE TABLE BILLING (
    billing_id INT AUTO_INCREMENT PRIMARY KEY,
    billing_date DATE,
    payment_method VARCHAR(50),
    goods_or_services TEXT,
    customer_id INT NOT NULL,
    billing_staff_id INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id),
    FOREIGN KEY (billing_staff_id) REFERENCES EMPLOYEE(employee_id)
);

CREATE TABLE SALE (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    sale_date DATE NOT NULL,
    temporary_tag_number VARCHAR(20),
    customization_work TEXT,
    billing_id INT, -- Allows NULL for pending bills
    customer_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    salesperson_id INT NOT NULL,
    FOREIGN KEY (billing_id) REFERENCES BILLING(billing_id),
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id),
    FOREIGN KEY (vehicle_id) REFERENCES VEHICLE(vehicle_id),
    FOREIGN KEY (salesperson_id) REFERENCES EMPLOYEE(employee_id)
);

CREATE TABLE SERVICE (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    arrival_mileage INT,
    departure_mileage INT,
    preliminary_estimate DECIMAL(10, 2),
    work_performed TEXT,
    billing_id INT, -- Allows NULL for pending bills
    customer_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    FOREIGN KEY (billing_id) REFERENCES BILLING(billing_id),
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id),
    FOREIGN KEY (vehicle_id) REFERENCES VEHICLE(vehicle_id)
);

CREATE TABLE SERVICE_ASSIGNMENT (
    service_assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    service_id INT NOT NULL,
    mechanic_id INT NOT NULL,
    FOREIGN KEY (service_id) REFERENCES SERVICE(service_id) ON DELETE CASCADE,
    FOREIGN KEY (mechanic_id) REFERENCES EMPLOYEE(employee_id)
);