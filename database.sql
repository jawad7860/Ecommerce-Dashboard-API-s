-- Check if the database exists and drop it if it does
DROP DATABASE IF EXISTS ecom_dashboard;

-- Create a new database
CREATE DATABASE ecom_dashboard;

-- Use the newly created database
USE ecom_dashboard;

-- Create the Categories table
CREATE TABLE Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create the Products table
CREATE TABLE Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

-- Create the Sales table
CREATE TABLE Sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    sale_date DATETIME NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Create the Inventory table
CREATE TABLE Inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    stock_quantity INT NOT NULL,
    low_stock_threshold INT,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Optional: Create an index on product names for faster searches
CREATE INDEX idx_product_name ON Products(name);

-- Optional: Create an index on sale dates for faster sales analysis queries
CREATE INDEX idx_sale_date ON Sales(sale_date);

-- Insert 10 entries of dummy data into Categories table
INSERT INTO Categories (name) VALUES
    ('Category 1'),
    ('Category 2'),
    ('Category 3'),
    ('Category 4'),
    ('Category 5'),
    ('Category 6'),
    ('Category 7'),
    ('Category 8'),
    ('Category 9'),
    ('Category 10');

-- Insert 10 entries of dummy data into Products table
INSERT INTO Products (name, price, category_id) VALUES
    ('Product 1', 10.99, 1),
    ('Product 2', 25.50, 2),
    ('Product 3', 5.99, 1),
    ('Product 4', 12.75, 3),
    ('Product 5', 19.99, 2),
    ('Product 6', 8.49, 1),
    ('Product 7', 14.95, 4),
    ('Product 8', 7.99, 3),
    ('Product 9', 29.99, 5),
    ('Product 10', 11.25, 4);

-- Insert 10 entries of dummy data into Sales table
INSERT INTO Sales (product_id, sale_date, quantity) VALUES
    (1, '2023-10-01 10:00:00', 5),
    (2, '2023-10-02 11:00:00', 3),
    (3, '2023-09-15 14:30:00', 10),
    (4, '2023-08-20 09:45:00', 8),
    (5, '2023-07-05 16:20:00', 12),
    (6, '2023-06-12 12:15:00', 7),
    (7, '2023-05-03 13:55:00', 6),
    (8, '2023-04-18 08:30:00', 4),
    (9, '2023-03-09 18:10:00', 11),
    (10, '2023-02-24 17:40:00', 9);

-- Insert 10 entries of dummy data into Inventory table
INSERT INTO Inventory (product_id, stock_quantity, low_stock_threshold) VALUES
    (1, 50, 10),
    (2, 20, 5),
    (3, 100, 20),
    (4, 30, 8),
    (5, 15, 4),
    (6, 40, 12),
    (7, 60, 15),
    (8, 25, 6),
    (9, 35, 10),
    (10, 18, 7);

