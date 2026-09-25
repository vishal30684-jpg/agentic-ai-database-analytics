CREATE DATABASE IF NOT EXISTS agentic_ai_db;

USE agentic_ai_db;

-- Customers
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    city VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0
);

-- Orders
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'Pending',

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

-- Order Items
CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

-- Customers
INSERT INTO customers (name, email, city) VALUES
('Rahul Sharma', 'rahul@example.com', 'Delhi'),
('Priya Verma', 'priya@example.com', 'Mumbai'),
('Amit Singh', 'amit@example.com', 'Bangalore'),
('Neha Gupta', 'neha@example.com', 'Pune'),
('Rohit Kumar', 'rohit@example.com', 'Indore');

-- Products
INSERT INTO products (name, category, price, stock) VALUES
('Laptop', 'Electronics', 65000.00, 20),
('Monitor', 'Electronics', 15000.00, 30),
('Keyboard', 'Accessories', 2500.00, 50),
('Mouse', 'Accessories', 1200.00, 80),
('Headphones', 'Accessories', 3500.00, 40);

-- Orders
INSERT INTO orders (customer_id, status) VALUES
(1, 'Completed'),
(2, 'Completed'),
(3, 'Completed'),
(1, 'Completed'),
(4, 'Pending'),
(5, 'Completed');

-- Order Items
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 65000.00),
(1, 3, 2, 2500.00),

(2, 2, 1, 15000.00),
(2, 4, 2, 1200.00),

(3, 1, 1, 65000.00),
(3, 5, 1, 3500.00),

(4, 2, 2, 15000.00),

(5, 4, 1, 1200.00),

(6, 3, 1, 2500.00),
(6, 5, 1, 3500.00);