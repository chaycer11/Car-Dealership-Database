-- 1. Create the database
CREATE DATABASE IF NOT EXISTS car_dealership;
USE car_dealership;

CREATE TABLE Employee (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    phone VARCHAR(20),
    email varchar(255),
    role ENUM('mechanic', 'salesperson', 'billing')
);

CREATE TABLE Vehicle (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    vin VARCHAR(17) UNIQUE NOT NULL,
    make VARCHAR(50),
    MODEL VARCHAR(50),
    year INT,
    price DECIMAL(10, 2),
    status ENUM('available', 'sold', 'maintenance') DEFAULT 'available',
    location ENUM('main_lot', 'remote_lot', 'other_dealership', 'in_transit')
);

CREATE TABLE Customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    phone VARCHAR(20),
    email VARCHAR(255),
    customer_type ENUM('purchase', 'service', 'visit')
);

CREATE TABLE Billing (
    billing_id INT AUTO_INCREMENT PRIMARY KEY,
    billing_date DATE,
    payment_method ENUM('cash', 'credit_card', 'debit_card', 'check'),
    goods_or_services VARCHAR(50),
    amount DECIMAL(10, 2) NOT NULL,
    customer_id INT,
    billing_staff_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (billing_staff_id) REFERENCES Employee(employee_id)
);

CREATE TABLE Sale (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    sale_date DATE,
    temp_tag_num VARCHAR(20),
    customization_work VARCHAR(255),
    billing_id INT,
    customer_id INT,
    vehicle_id INT,
    salesperson_id INT,
    FOREIGN KEY (billing_id) REFERENCES Billing(billing_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id),
    FOREIGN KEY (salesperson_id) REFERENCES Employee(employee_id)
);

CREATE TABLE Service (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    arrival_mileage INT,
    departure_mileage INT,
    preliminary_estimate DECIMAL(10, 2),
    work_done VARCHAR(255),
    billing_id INT,
    customer_id INT,
    vehicle_id INT,
    FOREIGN KEY (billing_id) REFERENCES Billing(billing_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id)
);

CREATE TABLE Service_Assignment (
    service_assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    service_id INT,
    mechanic_id INT,
    FOREIGN KEY (service_id) REFERENCES Service(service_id),
    FOREIGN KEY (mechanic_id) REFERENCES Employee(employee_id)
);